#!/usr/bin/python
import MySQLdb
import etc

new_db_conn=MySQLdb.connect (host = etc.dbhost,db=etc.dbname,user="root",passwd="skidoo!")
new=new_db_conn.cursor()

new.execute("""
CREATE TABLE `emprunt` (
  `id` int(11) NOT NULL auto_increment,
  `return_date` datetime default NULL,
  `item_id` int(11) default NULL,
  `borrower_id` int(11) default NULL,
  `date` datetime default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
""")

new.execute("""
CREATE TABLE `member` (
  `id` int(11) NOT NULL auto_increment,
  `first_name` varchar(255) default NULL,
  `last_name` varchar(255) default NULL,
  `e_mail` varchar(255) default NULL,
  `phone` varchar(15) default NULL,
  `paid` varchar(5) default NULL,
  PRIMARY KEY  (`id`),
  KEY `e_mail` (`e_mail`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;""")
