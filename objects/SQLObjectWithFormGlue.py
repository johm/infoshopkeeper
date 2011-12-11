from sqlobject import *
from formencode import htmlfill
from datetime import date


class SQLObjectWithFormGlue(SQLObject):
    _cacheValues=False

    def form_to_object(myClass,formdata):
        try:
            obj=myClass.get(formdata['id'])
        except:
            obj=myClass()
        for col in obj.sqlmeta.columnList:
            try:
                value=formdata[col.name]
                if type(col) == SODateTimeCol:
                    if len(value)==10:
                        value=date(int(value[0:4]),int(value[5:7]),int(value[8:10]))
                        setattr(obj,col.name,value)
                else:
                    if type(col) == SOFloatCol:
                        value=float(value)
                    if type(col) == SOForeignKey or type(col) == SOIntCol:
                        value=int(value)
                    setattr(obj,col.name,value)
            except KeyError:
                pass
    
        return obj
    form_to_object=staticmethod(form_to_object)

    
    def object_to_form(self):
        formhtml = "<input type='hidden' name='id' value='%s' />" % (self.id)
        for c in self.sqlmeta.columnList:
            if type(c)==SOStringCol:
                formhtml = formhtml + self.handleString(c)
            if type(c)==SOBLOBCol:
                formhtml = formhtml + self.handleBlob(c)
            if type(c)==SOFloatCol:
                formhtml = formhtml + self.handleBlob(c)
            if type(c)==SODateTimeCol:
                formhtml = formhtml + self.handleDateTime(c)
            if type(c)==SOForeignKey:
                try:
                    if c.joinName in self.listTheseKeys:
                        formhtml = formhtml + self.handleForeignKey(c)
                except:
                    pass

        formhtml=formhtml+"<input class='submit' type='submit'><br />"
        return formhtml


    def handleForeignKey(self,col):
        colName=col.joinName
        exec ("from objects.%s import %s" %(colName,colName.capitalize()))
        
        colClass=eval(colName.capitalize())
        toObjects=list(colClass.select())
        form_fragment="<label class='textbox'>%s</label><SELECT name='%sID' class='textbox'>" %(colName,colName)
        for o in toObjects:
            equals_fragment=""
            try:
                if o.id==getattr(self,colName+"ID"):
                    equals_fragment="SELECTED='true'"
                form_fragment=form_fragment+"<OPTION value='%s' %s>%s</OPTION>" %(o.id,equals_fragment,o.kindName) #this is a hack right now and needs to be fixed with a "primary descriptor" member
                
            except:
                import sys
                print "Unexpected error:", sys.exc_info()[1]
        form_fragment=form_fragment+"</SELECT><br />"
        return form_fragment
        
    def handleString(self,col):
        # look at http://formencode.org/docs/htmlfill.html
        form_fragment = """<label class='textbox' for='id_%s'>
                             %s
                           </label>
                           <input class='textbox' type='text' name='%s' id='id_%s'/>
                           """ % (col.name,col.name,col.name,col.name)
        value=getattr(self,col.name)
        if 'tostring' in dir(value):
            print "converting"
            value=value.tostring()
        defaults =  {col.name:value}
        parser = htmlfill.FillingParser(defaults)
        parser.feed(form_fragment)
        parser.close()
        html_fragment=parser.text()
        return html_fragment+"<br />"
    
    def handleFloat(self,col):
        return self.handleString(col)

    def handleBlob(self,col):
        return self.handleString(col)

    def handleDateTime(self,col):
        return self.handleString(col)



    def safe(self,col):
        value=getattr(self,col)
        try:
            value=value.tostring()
        except:
            pass
        return value
