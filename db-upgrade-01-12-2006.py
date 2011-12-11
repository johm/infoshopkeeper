import MySQLdb
import etc

new_db_conn=MySQLdb.connect (host = etc.dbhost,db=etc.dbname,user="eeP",passwd="eep")
new=new_db_conn.cursor()

new.execute("alter table transactionLog add (id int primary key auto_increment)")

