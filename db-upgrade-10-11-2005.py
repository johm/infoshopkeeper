import MySQLdb
import etc

new_db_conn=MySQLdb.connect (host = etc.dbhost,db=etc.dbname,user="eeP",passwd="eep")
new=new_db_conn.cursor()

new.execute("create table kind (kind_name varchar(255),id int(11) primary key auto_increment)")
new.execute("alter table transactionLog add schedule varchar(255)")
new.execute("alter table transactionLog add owner varchar(255)")
new.execute("alter table book add owner varchar(255)")
new.execute("alter table book add notes varchar(255)")
