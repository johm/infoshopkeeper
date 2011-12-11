#!/usr/bin/python
import MySQLdb
import etc

new_db_conn=MySQLdb.connect (host = etc.dbhost,db=etc.dbname,user=etc.dbuser,passwd=etc.dbpass)


new=new_db_conn.cursor()

new.execute("""
CREATE TABLE `author_title` (
  `author_id` int(11) default NULL,
  `title_id` int(11) default NULL,
  `id` int(11) NOT NULL auto_increment,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1
""")

new.execute("""
RENAME TABLE author TO old_author
"""
)


new.execute("""
CREATE TABLE `author` (
`title_id` int(11) default NULL,
`author_name` varchar(255) default NULL,
`id` int(11) NOT NULL auto_increment,
PRIMARY KEY  (`id`),
KEY `title_id` (`title_id`),
FULLTEXT KEY `author_name` (`author_name`)
)ENGINE=MyISAM DEFAULT CHARSET=latin1""")


new.execute ("SELECT author_name,title_id,id FROM old_author")
rows = new.fetchall()		  
for row in rows:
  authorname=row[0]
  title_id=row[1]
  oldauthorid=row[2]
  print "Adapting old record for %s, %s" % (authorname,title_id)
  new.execute("SELECT id FROM author WHERE author_name=%s",(authorname))
  existing_author_records=new.fetchall()
  new_author_id=0
  if len(existing_author_records)>1:
    print "Anomalous author count for %s!" % (oldauthorid)
  if len(existing_author_records)==0:
    new.execute("INSERT INTO author (author_name) VALUES(%s)",authorname)
    new.execute("SELECT LAST_INSERT_ID()")    
    new_author_id=new.fetchone()[0]
  else:
    new_author_id=existing_author_records[0][0]

  if new_author_id==0:
    print "Anomalous new author id for %s!" % (oldauthorid)
  else:
    new.execute("INSERT INTO author_title (author_id,title_id) VALUES (%s,%s)",(new_author_id,title_id))
    print "Processed old record %s into new record %s (%s)" % (oldauthorid,new_author_id,authorname)


