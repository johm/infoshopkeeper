from infoshopkeeper_config import configuration
cfg = configuration()
dbtype = cfg.get("dbtype")
dbname = cfg.get("dbname")
dbhost = cfg.get("dbhost")
dbuser = cfg.get("dbuser")
dbpass = cfg.get("dbpass")

from sqlobject import *

if dbtype in ('mysql', 'postgres'):
    if dbtype is 'mysql':
        import MySQLdb as dbmodule
    elif dbtype is 'postgres':
        import psycopg as dbmodule
    #deprecate
    def connect():
        return dbmodule.connect (host=dbhost,db=dbname,user=dbuser,passwd=dbpass)


    def conn():
        return '%s://%s:%s@%s/%s?charset=utf8&sqlobject_encoding=utf8' % (dbtype,dbuser,dbpass,dbhost,dbname)

elif dbtype is 'sqlite':
    import os, time, re
    from pysqlite2 import dbapi2 as sqlite
    db_file_ext = '.' + dbtype
    if not dbname.endswith(db_file_ext):
        dbname+=db_file_ext
    dbpath = os.path.join(dbhost, dbname)
    
    def now():
        return time.strftime('%Y-%m-%d %H:%M:%S')
    
    def regexp(regex, val):
        print regex, val, bool(re.search(regex, val, re.I))
        return bool(re.search(regex, val, re.I))
    
    class SQLiteCustomConnection(sqlite.Connection):
        def __init__(self, *args, **kwargs):
            print '@@@ SQLiteCustomConnection: registering functions'
            sqlite.Connection.__init__(self, *args, **kwargs)
            SQLiteCustomConnection.registerFunctions(self)
        
        def registerFunctions(self):
            self.create_function("NOW", 0, now)
            self.create_function("REGEXP", 2, regexp)
            self.create_function("regexp", 2, regexp)
            #~ self.execute("SELECT * FROM title WHERE title.booktitle REGEXP 'mar'")
        registerFunctions=staticmethod(registerFunctions)
    
    #deprecate
    _conn=None
    def connect():
        import sqlobject
        
        #~ return sqlite.connect (database=dbpath)
        global _conn
        if not _conn:
            #~ _conn = sqlite.connect (database=dbpath)
            from objects.title import Title
            # can't use factory in URI because sqliteconnection doesn't share globals with us
            Title._connection._connOptions['factory'] = SQLiteCustomConnection
            # get the connection instance that sqlobject is going to use, so we only have one
            _conn = Title._connection.getConnection()
            # since a connection is made before we can set the factory, we have to register
            #  the functions here also
            SQLiteCustomConnection.registerFunctions(_conn)
        return _conn

    def conn():
        return '%s://%s?debug=t' % (dbtype,dbpath)
        #~ return '%s://%s?debug=t&factory=SQLiteCustomConnection' % (dbtype,dbpath)
