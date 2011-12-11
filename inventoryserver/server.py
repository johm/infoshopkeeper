import cherrypy

from Cheetah.Template import Template

from sqlobject.sqlbuilder import *

from components import db
from objects.title import Title
from objects.book import Book
from objects.author import Author
from objects.category import Category
from objects.kind import Kind
from objects.transaction import Transaction
from IndexTemplate import IndexTemplate
from SearchTemplate import SearchTemplate
from BookEditTemplate import BookEditTemplate
from TitleEditTemplate import TitleEditTemplate
from TitleListTemplate import TitleListTemplate
from AuthorEditTemplate import AuthorEditTemplate
from CategoryEditTemplate import CategoryEditTemplate
from KindEditTemplate import KindEditTemplate
from KindListTemplate import KindListTemplate
from ReportListTemplate import ReportListTemplate
from ReportTemplate import ReportTemplate
from TransactionsTemplate import TransactionsTemplate
from CartTemplate import CartTemplate
from CheckoutTemplate import CheckoutTemplate
from infoshopkeeper_config import configuration
cfg = configuration()

from MySQLdb import escape_string

import string
import re


    

           
class InventoryServer:
    def __init__(self):
        self.reportlist=[getattr(__import__('reports.'+x,globals(),{},[1]),x) for x in cfg.get("reports")]

        
        self._indextemplate = IndexTemplate()
        self._carttemplate = CartTemplate()
        self._checkouttemplate = CheckoutTemplate()
        self._searchtemplate = SearchTemplate()
        self._bookedittemplate = BookEditTemplate()
        self._authoredittemplate = AuthorEditTemplate()
        self._categoryedittemplate = CategoryEditTemplate()
        self._kindedittemplate = KindEditTemplate()
        self._kindlisttemplate = KindListTemplate()
        self._titleedittemplate = TitleEditTemplate()
        self._titlelisttemplate = TitleListTemplate()
        self._reportlisttemplate = ReportListTemplate()
        self._reporttemplate = ReportTemplate()
        self._transactionstemplate = TransactionsTemplate()

        self.conn=db.connect()
                
    def common(self):
        for x in [getattr(self,x) for x in dir(self) if 'template' in x]:
            x.lastsearch=cherrypy.session.get('lastsearch',False)
        
    def index(self,**args):
        self.common()
        cherrypy.session['c'] = cherrypy.session.get('c',0)+1
        print   cherrypy.session['c']
        return self._indextemplate.respond()

    def bookedit(self,**args):
        self.common()
        self._bookedittemplate.book=Book.form_to_object(Book,args)
        return self._bookedittemplate.respond()

    def authoredit(self,**args):
        self.common()
        self._authoredittemplate.author=Author.form_to_object(Author,args)
        return self._authoredittemplate.respond()

    def categoryedit(self,**args):
        self.common()
        self._categoryedittemplate.category=Category.form_to_object(Category,args)
        return self._categoryedittemplate.respond()

    def kindedit(self,**args):
        self.common()
        if ('kindName' in args.keys()):
            self._kindedittemplate.kind=Kind.form_to_object(Kind,args)
            return self.kindlist()
        else:
            self._kindedittemplate.kind=Kind.form_to_object(Kind,args)
            return self._kindedittemplate.respond()
        


    def kindlist(self,**args):
        self.common()
        self._kindlisttemplate.kinds=list(Kind.select())
        return self._kindlisttemplate.respond()


    def titleedit(self,**args):
        self.common()
        self._titleedittemplate.title=Title.form_to_object(Title,args)
        return self._titleedittemplate.respond()

    def titlelist(self,**args):
        self.common()
        self._titlelisttemplate.titles=[]
        try:
            if type(args['titles']) == type("string"):
                self._titlelisttemplate.titles.append(Title.get(args['titles']))
            else:
                for id in args['titles']:
                    self._titlelisttemplate.titles.append(Title.get(id))
        except KeyError:
            pass

        try: 
            if (args['delete']):
            #delete the titles
                for title in self._titlelisttemplate.titles:
#                    for author in title.author:
#                        Author.delete(author.id)
                    for book in title.books:
                        Book.delete(book.id)
                    for category in title.categorys:
                        Category.delete(category.id)
                    
                    Title.delete(title.id)

            #and back to the search
                from cherrypy.lib import httptools
                httptools.redirect(cherrypy.session['lastsearch'])	
        except:
            return self._titlelisttemplate.respond()

    def checkout(self,**args):
        self.common()
        self._checkouttemplate.status_from=args.get("status_from","STOCK")
        self._checkouttemplate.status_to=args.get("status_to","RETURNED")
        self._checkouttemplate.schedules = [("list price",1)]+cfg.get("multiple_prices")
        
        if "change" in args:
            return self.addtocart(**args)
        if "finalize" in args:
            schedule_name=args["schedule"]
            schedule=[x for x in cfg.get("multiple_prices")+[("list price",1)] if x[0]==schedule_name] 
            schedule_price=schedule[0][1]
            receipt=""
            for q in cherrypy.session.get('quantities',[]):

                original=q[0]
                howmany=q[1]
                
                for copy in list(Book.select(AND(Book.q.titleID==original.titleID,Book.q.status=="STOCK",Book.q.listprice==original.listprice)))[0:howmany]:
                    cursor=self.conn.cursor()
                    cursor.execute("""
                        INSERT INTO transactionLog SET
                        action = "SALE",
                        amount = %s,
                        cashier = %s,
                        date = NOW(),
                        info = %s,
                        schedule = %s,
                        owner = %s
                        """,(copy.listprice * schedule_price,args["cashier"],"[%s] %s" % (copy.distributor,copy.title.booktitle),schedule_name,copy.owner))
                    copy.sellme()
                    cursor.close()
                line_pt_1 =  "%s  X  %s  @ $%.2f * %i%%" % (original.title.booktitle[:25],howmany,original.listprice,schedule_price * 100)
                receipt=receipt+string.ljust(line_pt_1,50)+string.rjust("$%.2f" % (howmany*schedule_price*original.listprice),10)
            return receipt
        
        if "restatus" in args and "status_to" in args and "status_from" in args:
            for q in cherrypy.session.get('quantities',[]):
                original=q[0]
                howmany=q[1]
                for copy in list(Book.select(AND(Book.q.titleID==original.titleID,Book.q.status==args["status_from"],Book.q.listprice==original.listprice)))[0:howmany]:
                    
                    copy.status=args["status_to"]
                    
            cherrypy.session['quantities']=[]

        if "delete" in args:
            for q in cherrypy.session.get('quantities',[]):
                original=q[0]
                original_price=original.listprice
                original_status=original.status
                original_title_id=original.titleID
                howmany=q[1]
                for copy in list(Book.select(AND(Book.q.titleID==original_title_id,Book.q.status==original_status,Book.q.listprice==original_price)))[0:howmany]:
                    
                    Book.delete(copy.id)
                    
            cherrypy.session['quantities']=[]

            
        
        self._checkouttemplate.quantities=cherrypy.session.get('quantities',[])
        return self._checkouttemplate.respond()

    def addtocart(self,**args):
        self.common() 
        
        if args.get('reset_quantities')=="true":
            cherrypy.session['quantities']=[]

        #these are multiple copies of the same book
        for a in args.keys():
            match=re.compile("^select_x_like_(\d+)").match(a)
            if match:
                try:
                    number_of_copies_to_sell=int(args[a])
                    id=match.group(1)
                    original=Book.get(id)
                    try:
                        quantities=cherrypy.session.get('quantities',[])
                        quantities.append((original,number_of_copies_to_sell))
                        cherrypy.session['quantities']=quantities
                    except:
                        pass

                except Exception,e:
                    print str(e)

        #these are checked individual copies
        copy_ids=[]
        try:
            if type(args['copy_id'])==type([0,1]):
                for copy_id in args['copy_id']:
                    copy_ids.append(copy_id)
            else:
                copy_ids.append(args['copy_id'])
        except:
            pass

        for copy_id in copy_ids:
            quantities=cherrypy.session.get('quantities',[])
            quantities.append((Book.get(copy_id),1))
            cherrypy.session['quantities']=quantities

        if "checkout" in args:
            return self.checkout(**args)
        else:
            self._carttemplate.quantities=cherrypy.session.get('quantities',[])
            return self._carttemplate.respond()

            


    def search(self,title="",sortby="booktitle",distributor="",owner="",publisher="",author="",category="",out_of_stock='no',stock_less_than="",stock_more_than="",sold_more_than="",sold_less_than="",tag="",kind=""):
        cherrypy.session['lastsearch']=False
        self.common()
        cherrypy.session['lastsearch']=cherrypy.request.browserUrl
        
        self._searchtemplate.empty=True
        self._searchtemplate.title=title
        self._searchtemplate.author=author
        self._searchtemplate.category=category
        self._searchtemplate.distributor=distributor
        self._searchtemplate.owner=owner
        self._searchtemplate.publisher=publisher
        self._searchtemplate.out_of_stock=out_of_stock
        self._searchtemplate.stock_less_than=stock_less_than
        self._searchtemplate.stock_more_than=stock_more_than
        self._searchtemplate.sold_more_than=sold_more_than
        self._searchtemplate.sold_less_than=sold_less_than
        self._searchtemplate.tag=tag
        self._searchtemplate.kinds=list(Kind.select())
        self._searchtemplate.kind=kind
        the_kind=kind
        if type(the_kind) == type([1,2,3]):
            the_kind=the_kind[0]
        
        titles=[]
        fields=[title,author,category,distributor,owner,publisher,stock_less_than,stock_more_than,sold_more_than,sold_less_than,tag,kind]
        fields_used = [f for f in fields if f != ""]
        
        if len(fields_used)>0 or out_of_stock=="yes":
            self._searchtemplate.empty=False
            if len(author)>0:
                titles=Title.select("""
                title.kind_id = '%s' AND
                title.booktitle LIKE '%%%s%%' AND
                title.publisher LIKE '%%%s%%' AND
                title.tag LIKE '%%%s%%' AND
                book.title_id=title.id AND book.distributor LIKE '%%%s%%' AND
                book.owner LIKE '%%%s%%' AND
                author_title.title_id=title.id AND
                author_title.author_id=author.id AND
                author.author_name LIKE '%%%s%%'        
                """ % (escape_string(the_kind),escape_string(title),escape_string(publisher),escape_string(tag),escape_string(distributor),escape_string(owner),escape_string(author)),orderBy=sortby,clauseTables=['book','author','author_title'],distinct=True)

            else:
                if len(category)>0:
                    titles=Title.select("""
                    title.kind_id = '%s' AND
                    title.booktitle LIKE '%%%s%%' AND
                    title.publisher LIKE '%%%s%%' AND
                    title.tag LIKE '%%%s%%' AND
                    book.title_id=title.id AND book.distributor LIKE '%%%s%%' AND
                    book.owner LIKE '%%%s%%' AND
                    category.title_id=title.id AND category.category_name LIKE '%%%s%%'        
                """ % (escape_string(the_kind),escape_string(title),escape_string(publisher),escape_string(tag),escape_string(distributor),escape_string(owner),escape_string(category)),orderBy=sortby,clauseTables=['book','category'],distinct=True)
                else:
                
                    # do a less complicated query
                    titles=Title.select("""
                    title.kind_id = '%s' AND
                    title.booktitle LIKE '%%%s%%' AND
                    title.publisher LIKE '%%%s%%' AND
                    title.tag LIKE '%%%s%%' AND
                    book.title_id=title.id AND book.distributor LIKE '%%%s%%'
                    AND book.owner LIKE '%%%s%%'         
                    """ % (escape_string(the_kind),escape_string(title),escape_string(publisher),escape_string(tag),escape_string(distributor),escape_string(owner)),orderBy=sortby,clauseTables=['book'],distinct=True)
                
            if out_of_stock == 'yes':
                titles = [t for t in titles if t.copies_in_status("STOCK") == 0]

            if stock_less_than != "":
                titles = [t for t in titles if t.copies_in_status("STOCK") <= int(stock_less_than)]

            if stock_more_than != "":
                titles = [t for t in titles if t.copies_in_status("STOCK") >= int(stock_more_than)]
                        
            if sold_more_than != "":
                titles = [t for t in titles if t.copies_in_status("SOLD") >= int(sold_more_than)]

            if sold_less_than != "":
                titles = [t for t in titles if t.copies_in_status("SOLD") <= int(sold_less_than)]
            

        self._searchtemplate.titles=titles


        
        
        
        return  self._searchtemplate.respond()
    
    def transactions(self,**args):
        self.common()
        begin_date=args.get('begin_date','')
        end_date=args.get('end_date','')
        what=args.get('what','')
        action=args.get('action','SALE')
        deleteid=args.get('deleteid','0')
        if int(deleteid) >0:
            Transaction.delete(deleteid)
        
        
        self._transactionstemplate.begin_date=begin_date
        self._transactionstemplate.end_date=end_date
        self._transactionstemplate.what=what
        self._transactionstemplate.action=action

        self._transactionstemplate.transactions=[]
        if begin_date and end_date:
            self._transactionstemplate.transactions=list(Transaction.select("""
        transactionLog.date >= '%s' AND
        transactionLog.date <= ADDDATE('%s',INTERVAL 1 DAY) AND
        transactionLog.info LIKE '%%%s%%' AND
        transactionLog.action LIKE '%%%s%%'
                """ % (escape_string(begin_date),escape_string(end_date),escape_string(what),escape_string(action))))
            
        
                                                                        
        return  self._transactionstemplate.respond()

        

    def reports(self,**args):
        self.common()
        self._reportlisttemplate.reports=[r.metadata for r in self.reportlist]
        return  self._reportlisttemplate.respond()

    def report(self,**args):
        self.common()
        the_report=[r for r in self.reportlist if r.metadata['action']==args['reportname']][0](args)
        self._reporttemplate.report=the_report
        if args.get('query_made','no')=='yes':
            self._reporttemplate.do_query=True
            results=the_report.query(args)

            self._reporttemplate.results=the_report.format_results(results)
            if the_report.do_total:
                self._reporttemplate.total=the_report.get_total(results)
            else:
                self._reporttemplate.total=0
        else:
            self._reporttemplate.do_query=False
            
        return  self._reporttemplate.respond()




    transactions.exposed=True
    reports.exposed=True    
    report.exposed=True
    index.exposed = True
    search.exposed = True
    addtocart.exposed = True
    checkout.exposed = True
    bookedit.exposed = True
    authoredit.exposed = True
    categoryedit.exposed = True
    titleedit.exposed = True
    titlelist.exposed = True
    kindedit.exposed = True
    kindlist.exposed = True



