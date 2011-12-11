import MySQLdb
new_db_conn=MySQLdb.connect (host = "localhost",db="newtest",user="",passwd="")
new=new_db_conn.cursor()

new.execute("create fulltext index booktitle on title (booktitle)")
new.execute("create index isbn  on title (isbn)")
new.execute("create fulltext index publisher on title (publisher)")
new.execute("create fulltext index tag on title (tag)")

new.execute("create fulltext index author_name on author (author_name)")
new.execute("create index title_id on author (title_id)")


new.execute("create fulltext index category_name on category (category_name)")
new.execute("create index title_id on category (title_id)")

new.execute("create index status on book (status)")
new.execute("create fulltext index distributor on book (distributor)")
new.execute("create index title_id on book (title_id)")




 
