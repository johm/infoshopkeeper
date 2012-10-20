from time import time,asctime,localtime,sleep
import types,string

from pyaws import ecs
from etc import amazon_license_key
from objects.title import Title
from objects.book import Book
from objects.author import Author
from objects.category import Category
from objects.kind import Kind
from upc import upc2isbn
from sqlobject.sqlbuilder import Field, RLIKE, AND

class inventory:
    def __init__(self):
        x=1
       
        
    def lookup_by_isbn(self,number):
        isbn=""
        if len(number)==13 or len(number)==18:
            isbn=upc2isbn(number)
        else:
            isbn=number
        print "NUMBER was " +number+ ",ISBN was "+isbn
        if len(isbn)>0:
            #first we check our database
            titles =  Title.select(Title.q.isbn==isbn)
            print titles #debug
            self.known_title= False
            the_titles=list(titles)
            if len(the_titles) > 0:
                self.known_title= the_titles[0]
                ProductName = the_titles[0].booktitle.decode("unicode_escape")
		authors = [x.author_name.decode("unicode_escape") for x in the_titles[0].author]
                authors_as_string = string.join(authors,',')
                categories = [x.categoryName.decode("unicode_escape") for x in the_titles[0].categorys]
                categories_as_string = string.join(categories,',')
                if len(the_titles[0].books) > 0:
#                    ListPrice = the_titles[0].books[0].listprice
                    ListPrice = max([b.listprice for b in the_titles[0].books])
                else:
                    ListPrice = 0
                Manufacturer = the_titles[0].publisher.decode("unicode_escape")
                
            else: #we don't have it yet
                sleep(1) # so amazon doesn't get huffy 
                ecs.setLicenseKey(amazon_license_key)
                ecs.setSecretAccessKey('hCVGbeXKy2lWQiA2VWV8iWgti6s9CiD5C/wxL0Qf')
                ecs.setOptions({'AssociateTag':'someoneelse-21'})
                pythonBooks = ecs.ItemLookup(isbn,IdType="ISBN",SearchIndex="Books",ResponseGroup="ItemAttributes")
                if pythonBooks:
                    result={}
                    authors=[]
                    categories=[]
                    b=pythonBooks[0]

                    for x in ['Author','Creator']:
                        if hasattr(b,x):
                            if type(getattr(b,x))==type([]):
                                authors.extend(getattr(b,x))
                            else:
                                authors.append(getattr(b,x))
                    

                    authors_as_string = string.join(authors,',')
                    categories_as_string =""
                    


                    ProductName=""
                    if hasattr(b,'Title'):
                        ProductName=b.Title

                        
                    Manufacturer=""
                    if hasattr(b,'Manufacturer'):
                        Manufacturer=b.Manufacturer

                    ListPrice=""
                    if hasattr(b,'ListPrice'):
                        ListPrice=b.ListPrice.FormattedPrice

                    
            return {"title":ProductName,
                    "authors":authors,
                    "authors_as_string":authors_as_string,
                    "categories_as_string":categories_as_string,
                    "list_price":ListPrice,
                    "publisher":Manufacturer,
                    "isbn":isbn,
                    "known_title": self.known_title}
       
        
    def lookup_by_upc(self,upc):

        if len(upc)>0:
            #first we check our database
            titles =  Title.select(Title.q.isbn==upc)
            print titles #debug
            self.known_title= False
            the_titles=list(titles)
            if len(the_titles) > 0:
                self.known_title= the_titles[0]
                ProductName = the_titles[0].booktitle
                authors = [x.authorName for x in the_titles[0].authors]
                authors_as_string = string.join(authors,',')
                categories = [x.categoryName for x in the_titles[0].categorys]
                categories_as_string = string.join(categories,',')
                if len(the_titles[0].books) > 0:
                    ListPrice = the_titles[0].books[0].listprice
                else:
                    ListPrice = 0
                Manufacturer = the_titles[0].publisher
                
            else: #we don't have it yet
                sleep(1) # so amazon doesn't get huffy 
                amazon.setLicense(amazon_license_key)
                pythonItems = amazon.searchByUPC(upc)
                if pythonItems:
                    result={}
                    authors=[]
                    author_object="none"
                    categories=[]
                    b=pythonItems[0]
                    try:
                        author_object=b.Artists.Artist
                    except AttributeError:
                        author_object="none"
                    if type(author_object) in types.StringTypes:
                        authors.append(author_object)
                    else: 
                        authors=author_object
                    authors_as_string = string.join(authors,',')

                    for category in b.BrowseList.BrowseNode:
                        categories.append(category.BrowseName)

                    categories_as_string = string.join(categories,',')
                 
                    ProductName=""
                    try:
                        if b.ProductName:
                            ProductName=b.ProductName
                    except AttributeError:
                        x=1
                        
                    Manufacturer=""
                    try:
                        if b.Manufacturer:
                            Manufacturer=b.Manufacturer
                    except AttributeError:
                        x=1

                    ListPrice=""
                    try:
                        if b.ListPrice:
                            ListPrice=b.ListPrice
                    except AttributeError:
                        x=1

                    ReleaseDate=""
                    try:
                        if b.ReleaseDate:
                            ReleaseDate=b.ReleaseDate
                    except AttributeError:
                        x=1
                    
            return {"title":ProductName,
                    "authors":authors,
                    "authors_as_string":authors_as_string,
                    "categories_as_string":categories_as_string,
                    "list_price":ListPrice,
                    "publisher":Manufacturer,
                    "isbn":upc,
                    "known_title": self.known_title}


    def addToInventory(self,title="",status="STOCK",authors=[],publisher="",price="",isbn="",categories=[],distributor="",owner="",notes="",quantity=1,known_title=False,kind_name="",extra_prices={}):
        if not(known_title):
	    #add a title
            the_kinds=list(Kind.select(Kind.q.kindName==kind_name))
            kind_id = None
            if the_kinds:
                kind_id = the_kinds[0].id
	    known_title=Title(isbn=isbn, booktitle=title.encode("ascii", "backslashreplace"), publisher=publisher.encode("ascii", "backslashreplace"),tag=" ",kindID=kind_id)
            for rawAuthor in authors:
	    	author = rawAuthor.encode("ascii", "backslashreplace")
		theAuthors = Author.selectBy(author_name=author)
		theAuthorsList = list(theAuthors)
		if len(theAuthorsList) == 1:
		    known_title.addAuthor(theAuthorsList[0])
		elif len(theAuthorsList) == 0:
		    a = Author(author_name=author)
		    known_title.addAuthor(a)
		else:
		    # We should SQLDataCoherenceLost here
		    print "mmm... looks like you have multiple author of the sama name in your database..."
            for category in categories:
                Category(categoryName=category.encode("ascii", "backslashreplace"),title=known_title)

        for i in range(int(quantity)): 
            print distributor.encode('ascii', "backslashreplace")
            
            wholesale=0
            try:
                wholesale=extra_prices['wholesale']
            except:
                pass

	    b=Book(title=known_title,status=status.encode("ascii", "backslashreplace"), distributor=distributor.encode('ascii', "backslashreplace"),listprice=price,owner=owner.encode("ascii", "backslashreplace"),notes=notes.encode("ascii", "backslashreplace"),consignmentStatus="",wholesale=wholesale)
            b.extracolumns()
            for mp in extra_prices.keys():
                setattr(b,string.replace(mp," ",""),extra_prices[mp])



                
    def getInventory(self,queryTerms):
        keys=queryTerms.keys()
        
        isbnSelect=""
        kindSelect=""
        statusSelect=""
        titleSelect=""
        authorSelect=""
        categorySelect=""
        clauseTables=[]

        if "kind" in keys: # joins suck, avoid if possible
            kind_map={}
            for k in [(x.kindName,x.id) for x in list(Kind.select())]:
                kind_map[k[0]]=k[1]
            try:
                kind_id=kind_map[queryTerms['kind']]
                kindSelect=Book.sqlrepr(AND(Field("book","title_id")==Field("title","id"), Field("title","kind_id")==kind_id))
            except: 
                pass
            
        if 'status' in keys:
            statusSelect=Book.sqlrepr(Field("book","status")==queryTerms["status"])
            

        if ('title' in keys) or ('authorName' in keys) or ('kind' in keys) or ('categoryName' in keys) or ('isbn' in keys):
            clauseTables.append('title') 
            #we are going to need to do a join 

            if 'title' in keys:
                titleSelect=Book.sqlrepr(AND(Field("book","title_id")==Field("title","id"), RLIKE(Field("title","booktitle"), queryTerms["title"])))


            if 'isbn' in keys:
                titleSelect=Book.sqlrepr(AND(Field("book","title_id")==Field("title","id"), Field("title","isbn")==queryTerms["isbn"]))


            if 'authorName' in keys:
                #~ authorSelect="""book.title_id = title.id AND author.title_id=title.id AND author.author_name RLIKE %s""" % (Book.sqlrepr(queryTerms["authorName"]))    
                authorSelect=Book.sqlrepr(AND(Field("book","title_id")==Field("title","id"), Field("author","id")==Field("author_title","author_id"), Field("title","id")==Field("author_title","title_id"), RLIKE(Field("author","author_name"), queryTerms["authorName"])))
                clauseTables.append('author')
                clauseTables.append('author_title')
            
            if 'categoryName' in keys:
                #~ categorySelect="""book.title_id = title.id AND category.title_id=title.id AND category.category_name RLIKE %s""" % (Book.sqlrepr(queryTerms["categoryName"]))
                categorySelect=Book.sqlrepr(AND(Field("book","title_id")==Field("title","id"), Field("category","title_id")==Field("title","id"), RLIKE(Field("category","category_name"), queryTerms["categoryName"])))
                clauseTables.append('category')
       	# At this time, ubuntu install sqlobject 0.6.1 if apt-get install python2.4-sqlobject,
		# which make the search crash, since the distinct attribute is defined somewhere after 0.6.1 
        try:
        	books=Book.select(
				string.join([term for term in [statusSelect,titleSelect,authorSelect,kindSelect,categorySelect] if term !=""]," AND "),
				clauseTables=clauseTables,
				distinct=True	 )
        except TypeError:
        	books=Book.select(
				string.join([term for term in [statusSelect,titleSelect,authorSelect,kindSelect,categorySelect] if term !=""]," AND "),
				clauseTables=clauseTables	)
			
        
        results={}
        i=1
        for b in books:
            theTitle=b.title.booktitle.decode("unicode_escape")
            if b.notes == None:
                b.notes=""
            authorString=string.join([a.author_name.decode("unicode_escape") for a in b.title.author],",")
            results[i]=(string.capitalize(theTitle),
                        authorString, 
                        b.listprice,
                        b.title.publisher.decode("unicode_escape"),
                        b.status.decode("unicode_escape"),
                        b.title.isbn,
                        b.distributor.decode("unicode_escape"),
                        b.notes.decode("unicode_escape"),
                        b.id,
                        b.title.kind and b.title.kind.kindName or '')
            i=i+1                
        
        return results

    
