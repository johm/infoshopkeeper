#!/usr/bin/python

# Copyright 2007 Guillaume Beaulieu

# This file is part of Infoshopkeeper.

# Infoshopkeeper is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or any later version.

# Infoshopkeeper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Infoshopkeeper; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301
# USA


import MySQLdb
import sys
import os
import etc

print """
This should be safe. But I would backup my data before trying, since this
script will make modification on how every book is linked to his author,
which could possibly make a lot of damage. 

The way it works is by creating and intermediary table between the author
and the titles, so that an author can have multiple books, and a book can
have multiple authors. The script works by reading a line of the title
table, unioned with the author table, to put the title id and the book id
together in the author_title table. This was tested on sqlobject 0.9. 
This script rely on the way that sqlobject handle is object internally, 
so in case of problem, check the way sqlobject handle multiple relationship
on your version, and get the table fitted accordingly. (this should not
be required). Then the author database is verified to contain no duplicate
author.

However, this script was written carefully, and have been tested thouroughly.
It is avisable to not stop the script until the end once started, although
when the script is started and the table author_title already, it checks that
no books make infoshopkeeper have problem by having an title that have no 
author (that's why Anonymous will have written more books than Marx), and
fixes it assuming that the author_id is a reference to author.id (which
is the case, since this is written in the doc of sqlobject 0.9:

Note the column person = ForeignKey("Person"). This is a reference to a Person object. We refer to other classes by name (with a string). In the database there will be a person_id column, type INT, which points to the person column. )

As a part of a gpl program, this file come WITHOUT ANY WARRANTY ! 
However, I'll try to help out any infoshop whose database
get fucked up by my fault. 

AND DON'T FORGET TO BACKUP YOUR DATA !

Press ctrl-c to quit or <enter> to continue
"""
sys.stdin.read(1)
new_db_conn=MySQLdb.connect (host = etc.dbhost,db=etc.dbname,user=etc.dbuser,passwd=etc.dbpass)

def shrink(new_db_conn):
    shrinka=new_db_conn.cursor()
    # sql for get the count of all duplicated authors, and the number of the smallest author id
    # which got that name
    print("SELECT author_name, COUNT(author_name) AS num, min(author.id) FROM author GROUP BY author_name HAVING num > 1")
    shrinka.execute("SELECT author_name, COUNT(author_name) AS num, min(author.id) FROM author GROUP BY author_name HAVING num > 1")
    a = shrinka.fetchall()
    for b in a:
        print "The author %s is present %s time in the database. The lowest id of his occurence is %s" % (b[0], b[1], b[2])
        getWrongs=new_db_conn.cursor()
	# This select all author.id having the same name but which aren't the smallest id of the author name
	getWrongs.execute("SELECT DISTINCT author.id FROM author_title, author WHERE author.id = author_title.author_id AND author.author_name = \"%s\" AND author.id <> %s" %
		(b[0], b[2]))
	c = getWrongs.fetchall()
	if len(c) != b[1] - 1:
	    sys.exit("Something wrong happened (COUNT(author_name) = " + str(b[1]) + ", which is greater than the selection of things to modify (" + str(len(c)) + ")")
	for d in c:
	    update=new_db_conn.cursor()
	    update.execute("update author_title set author_title.author_id = \"%s\" where author_title.author_id =\"%s\"" % (b[2], d[0]))
	
        
    

new=new_db_conn.cursor()
new.execute("show tables")
sentinel = 0
for a in new.fetchall():
    if a[0] == "author_title":
        print "author_title does exist !"
	# The new table is already there, so we set the sentinel to 1
	sentinel = 1
	# And we check the integrity of the relations, to be sure that
	# every book is binded to an author. In the worse case scenario
	# the book is binded 
	integrity=new_db_conn.cursor()
	# We get every title.id that fits a author.title_id and is in author_title
	# We CAN'T select max(title.id) since there can be some id that have been added
	# in between...
	integrity.execute("SELECT title.id FROM title, author, author_title WHERE author.title_id = title.id AND title.id = author_title.title_id")
	allLinked = integrity.fetchall()
	the_list = []
	for iter in allLinked:
	    print iter[0]
	    the_list.append(str(iter[0]))
	the_stringed_list = ",".join(the_list)
	print the_stringed_list
	integrity=new_db_conn.cursor()
	integrity.execute("SELECT title.id FROM title WHERE title.id NOT IN (%s)" % the_stringed_list)
	allNotLinked = integrity.fetchall()
	for iter in allNotLinked:
            transferor=new_db_conn.cursor()
            transferor.execute("select author.id, title.id from title, author where author.title_id = title.id")
            allNotLinked = transferor.fetchall()
            print "adding " + str(len(allNotLinked)) + " links the multiple join !"
            for iter in allNotLinked:
	        #print iter
                adder=new_db_conn.cursor()
	        print("insert into author_title (author_id, title_id) values (\"%s\", \"%s\")" % (iter[0], iter[1]))
	        adder.execute("insert into author_title (author_id, title_id) values (\"%s\", \"%s\")" % (iter[0], iter[1]))
	shrink(new_db_conn)
	print "Done !"
	sys.exit(0)
	    

if sentinel==0:
    print "author_title doesn't exist"
    # We create the table
    new.execute("""
    CREATE TABLE `author_title` (
       `author_id` int(11) default NULL,
       `title_id` int(11) default NULL,
       `id` int(11) NOT NULL auto_increment,
       PRIMARY KEY  (`id`)
    ) TYPE=MyISAM;

    """)
    # and we take every book in the new table
    transferor=new_db_conn.cursor()
    transferor.execute("select author.id, title.id from title, author where author.title_id = title.id")
    allNotLinked = transferor.fetchall()
    print "adding " + str(len(allNotLinked)) + " links the multiple join !"
    for iter in allNotLinked:
	# print iter
        adder=new_db_conn.cursor()
	print("insert into author_title (author_id, title_id) values (\"%s\", \"%s\")" % (iter[0], iter[1]))
	adder.execute("insert into author_title (author_id, title_id) values (\"%s\", \"%s\")" % (iter[0], iter[1]))
print "Done adding the links to author_title, going to shrink the list of authors"	
shrink(new_db_conn)
print "Done !"
sys.exit(0)

