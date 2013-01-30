import MySQLdb
conn=MySQLdb.connect(host='localhost',user='sixu05202004',passwd='159357852',port=3306)
cur=conn.cursor()
conn.select_db('pythonpub')
cur.execute('select * from post')
result=cur.fetchall()
print result[0]



conn1=MySQLdb.connect(host='localhost',user='sixu05202004',passwd='159357852',port=3306)
cur1=conn1.cursor()
conn1.select_db('pythonpub1')
cur1.executemany('insert into post values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',result[0])
conn1.commit()

