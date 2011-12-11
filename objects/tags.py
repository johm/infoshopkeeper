import sys
import string


from sqlobject import *
from SQLObjectWithFormGlue import SQLObjectWithFormGlue
from mx.DateTime import now

from components import db
from infoshopkeeper_config import configuration
cfg = configuration()


class Tagable:
    
    
    def get_tags(self,category,key): 
        matching_tags = [t for t in self.tags if t.tagkey==key and t.tagcategory.description==category]
        return matching_tags

    def has_tag(self,category,key,date=None): 
        matching_tags = [t for t in self.tags if t.tagkey==key and t.tagcategory.description==category]
        if len(matching_tags)>0:
	   return True
	else:
	   return False


    def set_tag(self,category,key,value): 
        tag_category=None
        try:
            tag_category=Tagcategory.select(Tagcategory.q.description==category)[0]
        except:
            tag_category=Tagcategory(description=category)
        newtag=self.tagclass(tagkey=key,tagvalue=value,tagcategory=tag_category,parent=self)



    
    def get_unique_tag(self,category,key):
        matching_tags = [t for t in self.tags if t.tagkey==key and t.tagcategory.description==category]
        try:
            return matching_tags[0].tagvalue
        except:
            return ""

    def set_unique_tag(self,category,key,value):
        matching_tags = [t for t in self.tags if t.tagkey==key and t.tagcategory.description==category]
        if len(matching_tags)==0:
            tag_category=None
            try:
                tag_category=Tagcategory.select(Tagcategory.q.description==category)[0]
            except:
                tag_category=Tagcategory(description=category)
            newtag=self.tagclass(tagkey=key,tagvalue=value,tagcategory=tag_category,parent=self)

				
        else:
            tag=matching_tags[0]
            tag.tagvalue=value

    def get_tag_collection(self,category,key):
        matching_tags = [t for t in self.tags if t.tagkey==key and t.tagcategory.description==category]
        return [t.tagvalue for t in matching_tags]

    def set_tag_collection(self,category,key,values):
        matching_tags = [t for t in self.tags if t.tagkey==key and t.tagcategory.description==category]
        for t in matching_tags:
            t.destroySelf()
        tag_category=None

        try:
            tag_category=Tagcategory.select(Tagcategory.q.description==category)[0]
        except:
            tag_category=Tagcategory(description=category)
            
        for v in values:
            newtag=self.tagclass(tagkey=key,tagvalue=v,tagcategory=tag_category,parent=self)





class Booktag(SQLObjectWithFormGlue):
    _connection = db.conn() 
    when_tagged=DateCol(default=now)
    tagkey=StringCol()
    tagvalue=StringCol()
    tagcategory = ForeignKey('Tagcategory')
    parent = ForeignKey('Book',dbName='book_id')

class Titletag(SQLObjectWithFormGlue):
    _connection = db.conn() 
    when_tagged=DateCol(default=now)
    tagkey=StringCol()
    tagvalue=StringCol()
    tagcategory = ForeignKey('Tagcategory')
    parent = ForeignKey('Title',dbName='title_id')

class Tagcategory(SQLObjectWithFormGlue):
    _connection = db.conn() 
    description=StringCol() 
    




