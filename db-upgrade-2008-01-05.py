#!/usr/bin/python
import MySQLdb
import etc

new_db_conn=MySQLdb.connect (host = etc.dbhost,db=etc.dbname,user=etc.dbuser,passwd=etc.dbpass)
new=new_db_conn.cursor()

new.execute("""
CREATE TABLE `booktag` (
  `id` int(11) NOT NULL auto_increment,
  `book_id` int(11) default NULL,
  `when_tagged` date default NULL,
  `tagkey` varchar(255) default NULL,
  `tagvalue` varchar(255) default NULL,
  `tagcategory_id` int(11) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
""")

new.execute("""
CREATE TABLE `tagcategory` (
  `id` int(11) NOT NULL auto_increment,
  `description` varchar(255) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=44 DEFAULT CHARSET=latin1;
""")


new.execute("""
CREATE TABLE `titletag` (
  `id` int(11) NOT NULL auto_increment,
  `title_id` int(11) default NULL,
  `when_tagged` date default NULL,
  `tagkey` varchar(255) default NULL,
  `tagvalue` varchar(255) default NULL,
  `tagcategory_id` int(11) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=102 DEFAULT CHARSET=latin1;
""")
