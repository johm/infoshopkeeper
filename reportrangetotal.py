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

import components.db
conn=components.db.connect()

cursor=conn.cursor()


if len(sys.argv) == 3: 
	date1=sys.argv[1]
	date2=sys.argv[2]		
	cursor.execute("SELECT sum(amount) from transactionLog where action='SALE' and date>=%s and date<=ADDDATE(%s,INTERVAL 1 DAY)  order by date",(date1,date2))



rows=cursor.fetchall()

total = 0

total = rows[0]
print "Total Sales:  %.2f" % total
