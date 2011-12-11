#!/usr/bin/python
# Copyright 2006 John Duda 

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

from string import rjust,ljust
import sys
import isbn
import components.db
conn=components.db.connect()

cursor=conn.cursor()

cursor.execute("SELECT * from title where isbn RLIKE '[0-9X][0-9X][0-9X][0-9X][0-9X][0-9X][0-9X][0-9X][0-9X][0-9X]'")

rows=cursor.fetchall()

total = 0

for r in rows:
	#print "Dealing with %s"  %r[1]
	if isbn.isValid(r[1]):
		prefix=r[1][:-1]
		cursor.execute("SELECT * from title where isbn RLIKE %s and not (isbn = %s)",('^%s' % prefix,r[1]))
		partial_matches=cursor.fetchall()
		if len(partial_matches)>1:
			print "WTF %s" % r[1]
		else: 
			if len(partial_matches)==1:
				print "FIXING ISBN r[1]"
				print "%s == %s?" % (r[2],partial_matches[0][2])
				print "%s == %s?" % (r[1],partial_matches[0][1])
				#grab bad_isbn
				#delete bad title entry
				#change
				cursor.execute("UPDATE author set title_id=%s where title_id=%s",(r[0],partial_matches[0][0]))
				cursor.execute("UPDATE author_title set title_id=%s where title_id=%s",(r[0],partial_matches[0][0]))
				cursor.execute("UPDATE book set title_id=%s where title_id=%s",(r[0],partial_matches[0][0]))
				cursor.execute("UPDATE cache set title_id=%s where title_id=%s",(r[0],partial_matches[0][0]))
				cursor.execute("UPDATE category set title_id=%s where title_id=%s",(r[0],partial_matches[0][0]))
				cursor.execute("UPDATE titletag set title_id=%s where title_id=%s",(r[0],partial_matches[0][0]))
				cursor.execute("DELETE FROM title where id=%s",partial_matches[0][0])
				
