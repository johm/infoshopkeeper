#!/usr/bin/python2.6
from string import rjust,ljust
import sys
import mx.DateTime

import components.db
conn=components.db.connect()

cursor=conn.cursor()

theDate=mx.DateTime.now()
#theDate=theDate-7
while theDate.day_of_week != 6:
	theDate=theDate+1

date=theDate.date

desc="total"

if len(sys.argv) == 1:
					
	statement="SELECT sum(amount) from transactionLog where action='SALE' and date>=%s and date<=ADDDATE(%s,INTERVAL 1 DAY)  order by date"

else:
	if len(sys.argv) == 2:
		desc=sys.argv[1]
		if desc== 'food':
			statement="SELECT sum(amount) from transactionLog where action='SALE' and not(info LIKE '%%:%%') and date>=%s and date<=ADDDATE(%s,INTERVAL 1 DAY)  order by date" 
		else:	
			statement="SELECT sum(amount) from transactionLog where action='SALE' and info LIKE %s and date>=%s and date<=ADDDATE(%s,INTERVAL 1 DAY)  order by date" 

	else:
		print "usage: reportweek.py (string)"
		sys.exit()


date2=theDate
date1=theDate-6

try:
	if len(sys.argv)==1 or desc=='food':
		cursor.execute(statement,(date1.date,date2.date))
	else:
		cursor.execute(statement,("%"+sys.argv[1]+"%",date1.date,date2.date))
		#print statement,"%"+sys.argv[1]+"%",date1.date,date2.date
	rows=cursor.fetchall()
	total=rows[0][0]
	print "%s: %.2f" % (ljust(desc,20),total)

except:
	pass



