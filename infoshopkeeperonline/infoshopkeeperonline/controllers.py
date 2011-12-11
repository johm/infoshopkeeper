from turbogears import controllers, expose, flash,paginate
from model import Visit, VisitIdentity,Group,User,Permission
from turbogears import identity, redirect, widgets,validators
from cherrypy import request, response,session,HTTPError
from sqlobject import *

from time import strftime,gmtime
import sys
sys.path.append('../../')
sys.path.append('../')
from objects.book import Book
from objects.title import Title
from objects.section import Section
from objects.author import Author
from objects.transaction import Transaction
from etc import sections

from components import db
from mx.DateTime import now



# from infoshopkeeperonline import json
# import logging
# log = logging.getLogger("infoshopkeeperonline.controllers")

from MySQLdb import escape_string

class PrivateBackend(controllers.Controller,identity.SecureResource):
    require=identity.in_group("admin")

    @expose(template="infoshopkeeperonline.templates.private.uncategorizedtitles")
    def uncategorized(self,letter=""):
        all_titles=[]
        if letter=="":
            all_titles=Title.select("kind_id=1",orderBy='booktitle')
        else:
            all_titles=Title.select("""kind_id=1 and booktitle LIKE '%s%%'""" % (escape_string(letter)),orderBy='booktitle')
                    
        return dict(titles=[t for t in all_titles if len(list(t.sections))==0])


    @expose(template="infoshopkeeperonline.templates.private.outofstocktitles")
    def outofstock(self,letter=""):
        all_titles=[]
        if letter=="":
            all_titles=Title.select("kind_id=1",orderBy='booktitle')
        else:
            all_titles=Title.select("""kind_id=1 and booktitle LIKE '%s%%'""" % (escape_string(letter)),orderBy='booktitle')
                    
        return dict(titles=[t for t in all_titles if t.copies_in_status("STOCK")==0])



    @expose(template="infoshopkeeperonline.templates.private.unconfirmedtitles")
    def unconfirmed(self,letter=""):
        all_titles=[]
        if letter=="":
            all_titles=Title.select("kind_id=1",orderBy='booktitle')
        else:
            all_titles=Title.select("""kind_id=1 and booktitle LIKE '%s%%'""" % (escape_string(letter)),orderBy='booktitle')
        unconfirmed_titles=[]
        for t in all_titles:
            if t.copies_in_status('STOCK')>0:# or t.copies_in_status('UNKNOWN')>0:
                t.unconfirmed_books=[]
                for b in [b for b in t.books if (b.status=='STOCK' or b.status=='UNKNOWN')]:
                    tags=b.get_tags('inventory','confirmation11')  #needs a date eventually!
                    if len(tags)==0:
                        t.unconfirmed_books.append(b)
                if len(t.unconfirmed_books)>0:
                    unconfirmed_titles.append(t)
                    
        return dict(titles=unconfirmed_titles)

    @expose()
    def persistsection(self,section,activate):
        if not(session.has_key('persisting_sections')):
            session['persisting_sections']=[]
        if activate=='true':
            session['persisting_sections'].append(section)
        else:
            session['persisting_sections'].remove(section)
        return "OK"
        
    @expose(template="infoshopkeeperonline.templates.private.reinventory")
    def reinventory(self,isbn="",author="",title=""):
        searchform = widgets.TableForm(fields=PrivateSearchFields(), submit_text="Search!")
        if author == "" and title=="" and isbn=="":
            the_titles=False
        else:
            the_titles=Title.select("""
            title.isbn LIKE '%%%s%%' AND
            author.id=author_title.author_id AND
            author_title.title_id=title.id AND author.author_name LIKE '%%%s%%' AND title.booktitle LIKE '%%%s%%'
            """ % (escape_string(isbn),escape_string(author),escape_string(title)),orderBy="booktitle",clauseTables=['author','author_title'],distinct=True)
		
	title_count=0
	try:
		title_count=the_titles.count()
	except:
		pass
        if title_count>0:
            if the_titles.count()==1:
                return self.title(the_titles[0].id,searchvalues=dict(author=author,title=title,isbn=isbn))

        return dict(the_titles=the_titles,authorswidget=PrivateAuthorsWidget(),titlelistwidget=PrivateTitleListWidget(),searchform=searchform,values=dict(author=author,title=title,isbn=isbn))

    @expose(template="infoshopkeeperonline.templates.private.title")
    def title(self,id,searchvalues=None):
        thetitle=Title.get(id)
        searchform = widgets.TableForm(fields=PrivateSearchFields(), submit_text="Search!")
        titleform = widgets.TableForm(name="titleform",fields=PrivateTitleFields(), submit_text="modify this title's sections and distributor")
        titlepersistenceform = widgets.TableForm(fields=PrivateTitlePersistenceFields(), submit_text="")
        persisting_sections=[]
        #       try:
        #           persisting_sections=session['persisting_sections']
        #       except:
        #           session['persisting_sections']=[]
        #       print persisting_sections 
        #        sections=list(set(thetitle.get_tag_collection(category='inventory',key='section')))
        #        sections=thetitle.sections
        #      sections.extend(persisting_sections)
        print [s.id for s in list(thetitle.sections)]
        
        return dict(thetitle=thetitle,authorswidget=PrivateAuthorsWidget(),searchform=searchform,searchvalues=searchvalues,titleform=titleform,today=strftime("%Y-%m-%d", gmtime()),titlepersistenceform=titlepersistenceform,titlesections=[s.id for s in list(thetitle.sections)],persisting_sections=persisting_sections)


    @expose(template="infoshopkeeperonline.templates.private.checktrans")
    def checktrans(self,what):
        transactions=Transaction.select("""info LIKE '%%%s%%'""" % (escape_string(what)),orderBy='date')
        return dict(transactions=transactions)

    @expose()
    def reordertag(self,title_id):
	title=Title.get(title_id)
	title.set_tag(category="inventory",key="reorder",value=identity.current.user_name)
	return "1"

    @expose()
    def statustag(self,book_id,status):
	book=Book.get(book_id)
        if status == "CONFIRM":
            book.status="STOCK"
            book.set_tag(category="inventory",key="confirmation11",value="stock")
        else:
            if status=="SOLD":
                book.sold_when=now()
                book.status="SOLD"
                book.set_tag(category="inventory",key="confirmation11",value="sold_at_some_point")
            else:
                book.status=status
                book.set_tag(category="inventory",key="confirmation11",value="removed")
	return book.status

    @expose()
    def confirm(self,title,book,**kw):
        book=Book.get(book)
        title=Title.get(title)
        book.set_tag(category="inventory",key="confirmation11",value="stock")
        return self.title(title.id)

    @expose(template="infoshopkeeperonline.templates.private.section")
    def section(self,section_id,**kw):
        section=Section.get(section_id)
        return dict(section=section)
            
    @expose()
    def edit_title(self,title_id,**kw):
        title=Title.get(title_id)
        if kw['preferred_distributor']:
            title.set_unique_tag(category='distribution',key='preferred',value=kw['preferred_distributor'])
        if kw.has_key('sections'):
            the_sections=kw['sections']
            if type(the_sections) != type([0,1]):
                the_sections=[the_sections]
            #title.set_tag_collection(category='inventory',key='section',values=the_sections)
            for s in title.sections:
                print "Removing %s" % s 
                title.removeSection(s)
            for s in the_sections:
                print "Adding %s" % s 
                title.addSection(Section.get(s))
            
        return self.title(title_id)


class Root(controllers.RootController):
    @expose(template="infoshopkeeperonline.templates.welcome")
    # @identity.require(identity.in_group("admin"))
    def index(self):
        return self.storefront()
#        import time
        # log.debug("Happy TurboGears Controller Responding For Duty")
#        flash("Your application is now running")
#        return dict(now=time.ctime())



    @expose(template="infoshopkeeperonline.templates.login")
    def login(self, forward_url=None, previous_url=None, *args, **kw):

        if not identity.current.anonymous \
            and identity.was_login_attempted() \
            and not identity.get_identity_errors():
            raise redirect(forward_url)

        forward_url=None
        previous_url= request.path

        if identity.was_login_attempted():
            msg=_("The credentials you supplied were not correct or "
                   "did not grant access to this resource.")
        elif identity.get_identity_errors():
            msg=_("You must provide your credentials before accessing "
                   "this resource.")
        else:
            msg=_("Please log in.")
            forward_url= request.headers.get("Referer", "/")
            
        response.status=403
        return dict(message=msg, previous_url=previous_url, logging_in=True,
                    original_parameters=request.params,
                    forward_url=forward_url)

    @expose()
    def logout(self):
        identity.current.logout()
        raise redirect("/")



    #private stuff
    private=PrivateBackend()
        

    #public stuff


    @expose(template="infoshopkeeperonline.templates.sections")	
    def sections(self):
        return dict(authorswidget=AuthorsWidget(),titlelistwidget=TitleListWidget(),sections=Section.select("1=1",orderBy="section_name"),the_sections=False)

    @expose(template="infoshopkeeperonline.templates.section")	
    def section(self,section=None):
        the_section=Section.get(section)
        titles_in_section=[t for t in the_section.titles if t.copies_in_status("STOCK")>0]   
        titles_in_section.sort(key=lambda x: x.booktitle)
        #titles_in_section=Title.select("kind_id=1 and title.id=section_title.title_id and titletag.tagvalue='History' and titletag.tagkey='section'",clauseTables=["section_title"],orderBy="booktitle",distinct=True)
        return dict(authorswidget=AuthorsWidget(),titlelistwidget=TitleListWidget(),the_section=the_section,in_this_section=titles_in_section)


    @expose(template="infoshopkeeperonline.templates.authors")	
    def authors(self,letter=None):
        alphabet=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]      
        the_authors=False
        if letter != None:
            if letter in alphabet:
                the_authors=Author.select("""
                author.author_name RLIKE " %s[^ ]*$" AND
                   book.title_id=title.id AND
                   book.status ='STOCK' AND
                   author.id= author_title.author_id AND
                   author_title.title_id=title.id""" % (escape_string(letter)),orderBy="author_name",clauseTables=['book','title','author_title'],distinct=True)
            else:
                the_authors=Author.select("""
                author.author_name NOT RLIKE "^[:alpha:]" AND
                   book.title_id=title.id AND
                   book.status ='STOCK' AND
                   author.id=author_title.author_id AND
                   author_title.title_id=title.id""" ,orderBy="author_name",clauseTables=['book','title'],distinct=True)
            authors_for_letter=list(unique(the_authors))
            authors_for_letter.sort(sort_by_last_name)
            return dict(authorswidget=AuthorsWidget(),titlelistwidget=TitleListWidget(),the_authors=authors_for_letter,the_letter=letter,alphabet=alphabet)
        else:
            return dict(authorswidget=AuthorsWidget(),titlelistwidget=TitleListWidget(),the_authors=False,the_letter=letter,alphabet=alphabet)

    @expose(template="infoshopkeeperonline.templates.titles")	
    def titles(self,letter=None):
        alphabet=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]      
        the_titles=False
        if letter != None:
            if letter in alphabet:
                the_titles=Title.select("""
                   title.booktitle LIKE "%s%%" AND
                   book.title_id=title.id AND
                   book.status ='STOCK' """ % (escape_string(letter)),orderBy="booktitle",clauseTables=['book'],distinct=True)
            else:
                the_titles=Title.select("""
                   title.booktitle RLIKE "^[0-9]" AND
                   book.title_id=title.id AND
                   book.status ='STOCK' """ ,orderBy="booktitle",clauseTables=['book'],distinct=True)
            return dict(authorswidget=AuthorsWidget(),titlelistwidget=TitleListWidget(),the_titles=the_titles,the_letter=letter,alphabet=alphabet)
        else:
            return dict(authorswidget=AuthorsWidget(),titlelistwidget=TitleListWidget(),the_titles=False,the_letter=letter,alphabet=alphabet)


	
    @expose(template="infoshopkeeperonline.templates.storefront")
    def storefront(self):
        searchform = widgets.TableForm(fields=SearchFields(), submit_text="Search!")
        conn=db.connect()
        cursor=conn.cursor()
        cursor.execute("""
        select booktitle,count(book.id) as blah,title_id   from book,title where book.title_id=title.id and book.status='SOLD' and title.kind_id=1 group by title_id order by blah desc limit 30
        """)
        results= cursor.fetchall()
        cursor.close()
        
        best_sellers = [Title.get(x[2]) for x in results if Title.get(x[2]).copies_in_status("STOCK")>0]
        
        new_titles=Title.select("""
            book.title_id=title.id AND
            book.status ='STOCK'
            """ ,orderBy="-title.id",clauseTables=['book'],distinct=True)
        return dict(authorswidget=AuthorsWidget(),titlelistwidget=TitleListWidget(),searchform=searchform,new_titles=new_titles[:10],best_sellers=best_sellers)


    @expose(template="infoshopkeeperonline.templates.search")
    def search(self,author="",title=""):
        searchform = widgets.TableForm(fields=SearchFields(), submit_text="Search!")
        if author == "" and title=="":
            the_titles=False
        else:
            the_titles=Title.select("""
	    book.title_id=title.id AND
            book.status ='STOCK' AND
            author.id=author_title.author_id AND
            author_title.title_id=title.id AND author.author_name LIKE '%%%s%%' AND title.booktitle LIKE '%%%s%%'
            """ % (escape_string(author),escape_string(title)),orderBy="booktitle",clauseTables=['book','author','author_title'],distinct=True)
	return dict(the_titles=the_titles,authorswidget=AuthorsWidget(),titlelistwidget=TitleListWidget(),searchform=searchform,values=dict(author=author,title=title))
    
    @expose(template="infoshopkeeperonline.templates.author")
    def author(self,id):
    	the_author=Author.get(id)
	the_titles=Title.select("""
	    book.title_id=title.id AND
            book.status ='STOCK' AND
            author.id=author_title.author_id AND
            author_title.title_id=title.id AND author.author_name='%s'
            """ % (escape_string(the_author.author_name)),orderBy="booktitle",clauseTables=['book','author','author_title'],distinct=True)
	return dict(the_titles=the_titles,the_author=the_author,authorswidget=AuthorsWidget(),titlelistwidget=TitleListWidget())

    @expose(template="infoshopkeeperonline.templates.title")
    def title(self,id):
        ratingsform = widgets.RemoteForm(fields=RatingFields(), submit_text="Rate it!")
#        Title.sqlmeta.addJoin(MultipleJoin('Rating',joinMethodName='ratings'))
        thetitle=Title.get(id)
        thetitle.ratings=[]
        same_author=[]
        for author in thetitle.author:
            titles=Title.select("""
            title.id!=%s AND
            book.title_id=title.id AND
            book.status ='STOCK' AND
            author.id=author_title.author_id AND
            author_title.title_id=title.id AND author.author_name='%s'
            """ % (escape_string("%s" % thetitle.id),escape_string(author.author_name)),orderBy="booktitle",clauseTables=['book','author','author_title'],distinct=True)
            for title in titles:
	    	same_author.append(title)
        if thetitle.copies_in_status("STOCK")==0:
            raise HTTPError(404)
        
        return dict(thetitle=thetitle,authorswidget=AuthorsWidget(),ratingsform=ratingsform,titlelistwidget=TitleListWidget(),same_author=same_author)

    @expose()	
    def submit_rating(self, **kw):
        """ Echo the parameters back as html."""
        r=Rating(title=kw['title'],rater=kw['rater'],score=int(kw['score']),comments=kw['comments'])
        return "<div>Recieved data:<br>%r</br></div>" % kw


class SearchFields(widgets.WidgetsList):
    author  = widgets.TextField()
    title   = widgets.TextField()

class PrivateTitleFields(widgets.WidgetsList):
    import operator
    preferred_distributor=widgets.TextField()
    title_id=widgets.HiddenField()
    all_sections=[(l.id,l.sectionName) for l in list(Section.select())]
    all_sections.sort(key=operator.itemgetter(1))
    sections=widgets.CheckBoxList(options=all_sections,field_class='inline')

class PrivateTitlePersistenceFields(widgets.WidgetsList):
    sections.sort()
    sections=widgets.CheckBoxList(label="Persistent Sections",options=sections,field_class='inline')


    
class PrivateSearchFields(widgets.WidgetsList):
    isbn=widgets.TextField()
    author  = widgets.TextField()
    title   = widgets.TextField()
    

class RatingFields(widgets.WidgetsList):
    rater = widgets.TextField(validators=validators.NotEmpty)
    score = widgets.RadioButtonList(options=[(1, "1"),
                                             (2, "2"),
                                             (3, "3"),
                                             (4, "4"),
                                             (5, "5")],
                                    default=5,attrs={'class':'ratingsform'})
    comments=widgets.TextArea()
    title=widgets.HiddenField()

def sort_by_last_name(x,y):
    x_words=x.author_name.split()
    y_words=y.author_name.split()
    x_last=x_words[-1:]
    y_last=y_words[-1:]
    if x_last<y_last:
        return -1
    elif x_last>y_last:
        return 1
    else:
        x_first=x_words[0]
        y_first=y_words[0]
        if x_first<y_first:
            return -1
        elif x_first>y_first:
            return 1
        else:
            return 0


def unique(seq):
    seen = []
    return (c for c in seq if not (c.author_name in seen or seen.append(c.author_name)))
    
class AuthorsWidget(widgets.Widget):
      template = 'infoshopkeeperonline.templates.authorswidget'

class PrivateAuthorsWidget(widgets.Widget):
      template = 'infoshopkeeperonline.templates.private.authorswidget'

class TitleListWidget(widgets.Widget):
    template = 'infoshopkeeperonline.templates.itemtitlelistwidget'

class PrivateTitleListWidget(widgets.Widget):
    template = 'infoshopkeeperonline.templates.private.itemtitlelistwidget'
      
      
class TitleWidget(widgets.Widget):
      template = 'infoshopkeeperonline.templates.itemtitlewidget'



      
