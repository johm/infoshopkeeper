Here's how the upgrade works.


1) Install new dependencies

a) SQLObject 0.6.1  from http://sqlobject.org

download from here:
http://prdownloads.sourceforge.net/sqlobject/SQLObject-0.6.1.tar.gz?download

you'll need to patch the converters.py file(after installing) to work
around a mysql bug

Replace the StringLikeConverter function with:


from array import array
def StringLikeConverter(value, db):
    if type(value) == type(array('c','')):
        try:
            value = value.tounicode()
        except ValueError:
            value = value.tostring()

    if db in ('mysql', 'postgres'):
        for orig, repl in sqlStringReplace:
            value = value.replace(orig, repl)
    elif db in ('sqlite', 'firebird', 'sybase', 'maxdb'):
        value = value.replace("'", "''")
    else:
        assert 0, "Database %s unknown" % db
    return "'%s'" % value

registerConverter(type(""), StringLikeConverter)
registerConverter(type(u""), StringLikeConverter)
registerConverter(type(array('c','')), StringLikeConverter)

(apparently this is fixed in subversion, as well.)

b) CherryPy version 2.0 from http://www.cherrypy.org

c) Cheetah (python templating engine), any recent version should work
   ok. see http://www.cheetahtemplate.org
   
d) formencode (a small libary to handle some html-escaping issues)
   http://formencode.org/ (written by Ian Bicking, who also did
   SQLObject)

   get it with subversion by: 
svn co http://svn.colorstudy.com/FormEncode/trunk FormEncode

e) mx.DateTime http://www.egenix.com/files/python/mxDateTime.html


2) create a new database to hold the converted data.


3) fill in the connection info for your old and new databases in
   db-upgrade-08-15-2005.py and run this.

4) copy cherrypy.conf-dist to cherrypy.conf and customize this with
   proper directories for your install.  switch etc.py to the new db,
   and make sure to add the line from etc.py-dist that points to the
   cherrypy.conf file you just made.


6) to use the inventory browser, run ./server and go to localhost:8080




