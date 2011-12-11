import MySQLdb

old_db_conn=MySQLdb.connect (host = "localhost",db="oldtest",user="",passwd="")

new_db_conn=MySQLdb.connect (host = "localhost",db="newtest",user="",passwd="")


old=old_db_conn.cursor()
old.execute("update inventory set distributor='' where distributor is NULL") #fix stuff up

new=new_db_conn.cursor()


def do_the_books():
    old.execute("SELECT * from inventory")
    oldbooks=old.fetchall()
    for oldbook in oldbooks:
        #check for new title
        #do we have an isbn?
        old_id=oldbook[0]
        isbn=oldbook[1]
        title=oldbook[2]
        publisher=oldbook[3]
        listprice=oldbook[4]
        inventoried_when=oldbook[6]
        status=oldbook[10]
        distributor=oldbook[11]

        newtitles=[]
        newtitleid=0
        if isbn == "":
            new.execute("SELECT * from title where booktitle=%s",(title))
            newtitles=new.fetchall()
        else:
            new.execute("SELECT * from title where isbn=%s",(isbn))
            newtitles=new.fetchall()
            
        if len(newtitles) ==0:
            print "adding title"
            #we need to add this title
            new.execute("INSERT INTO title values ('',%s,%s,%s,'','')",(isbn,title,publisher))
            newtitleid=new_db_conn.insert_id()
            #do the authors
            old.execute("SELECT * from authors where bookID=%s",(old_id))
            for a in old.fetchall():
                new.execute("INSERT INTO author VALUES (%s,%s,'')",(newtitleid,a[1]))
                        
            #do the categories
            old.execute("SELECT * from categories where bookID=%s",(old_id))
            for c in old.fetchall():
                new.execute("INSERT INTO category VALUES (%s,%s,'')",(newtitleid,c[1]))

        else:
            newtitleid=newtitles[0][0]
            #we have this title already(or we do now!)

        #do the books(i.e. copies)
        new.execute("INSERT into book VALUES ('',%s,'',%s,'book','',%s,%s,%s,%s)",(listprice,inventoried_when,status,distributor,newtitleid,''))  #sold_when may require a manual fix

        
    

def move_unchanged_data():
    old.execute("SELECT * from cashbox")
    cashbox_rows=old.fetchall()
    for r in cashbox_rows:
        new.execute("INSERT INTO cashbox values (%s,%s)",(r[0],r[1]))

    old.execute("SELECT * from notes")
    notes_rows=old.fetchall()
    for r in notes_rows:
        new.execute("INSERT INTO notes values (%s,%s,%s)",(r[0],r[1],r[2]))

    old.execute("SELECT * from transactionLog")
    log_rows=old.fetchall()
    for r in log_rows:
        new.execute("INSERT INTO transactionLog values (%s,%s,%s,%s,%s)",(r[0],r[1],r[2],r[3],r[4]))
    

    

def create_new_tables():
    new.execute("""
    CREATE TABLE `author` (
    `title_id` int(11) default NULL,
    `author_name` varchar(255) default NULL,
    `id` int(11) NOT NULL auto_increment,
    PRIMARY KEY  (`id`)
    ) 
    """)
    
    
    new.execute("""
    CREATE TABLE `book` (
    `id` int(11) NOT NULL auto_increment,
    `listprice` float default NULL,
    `consignment_status` varchar(255) default NULL,
    `inventoried_when` date default NULL,
    `type` varchar(50) default NULL,
    `location` varchar(50) default NULL,
    `status` varchar(255) default NULL,
    `distributor` text,
    `title_id` int(11) default NULL,
    `sold_when` date default NULL,
    PRIMARY KEY  (`id`)
    )
    """)
    
    
    new.execute("""
    CREATE TABLE `cashbox` (
    `amount` float default NULL,
    `date` datetime default NULL
    )
    """)
    
    
    new.execute("""
    CREATE TABLE `category` (
    `title_id` int(11) default NULL,
    `category_name` varchar(255) default NULL,
    `id` int(11) NOT NULL auto_increment,
    PRIMARY KEY  (`id`)
    )
    """)
    
    
    new.execute("""
    CREATE TABLE `notes` (
    `message` text,
    `author` varchar(32) default NULL,
    `whenEntered` datetime default NULL
    ) TYPE=MyISAM;
    
    """)
    
    new.execute("""
    CREATE TABLE `title` (
    `id` int(11) NOT NULL auto_increment,
    `isbn` varchar(10) default NULL,
    `booktitle` text,
    `publisher` text,
    `release_date` varchar(255) default NULL,
    `tag` text,
    PRIMARY KEY  (`id`)
    ) TYPE=MyISAM;
    """)
    
    new.execute("""
    CREATE TABLE `transactionLog` (
    `action` varchar(255) default NULL,
    `amount` float default NULL,
    `date` datetime default NULL,
    `cashier` varchar(255) default NULL,
    `info` blob
    )
    """)
    
    

print "creating new tables"
create_new_tables()

print "carrying over unchanged data"
move_unchanged_data()

print "converting inventory"
do_the_books()

print "faking sales dates"
new.execute("UPDATE book set sold_when=now() where status='SOLD'")
