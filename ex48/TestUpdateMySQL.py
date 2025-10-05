from MySQL.ex48.TestQueryMySQL import conn

cursor = conn.cursor()
sql = "update student set name = 'The Gioi Di Dong' where Code = 'sv09'"
cursor.execute(sql)

conn.commit()
print(cursor.rowcount, 'record(s) affected.')

cursor = conn.cursor()
sql="update student set name=%s where Code=%s"
val=('The Gioi Di Dong','sv09')

cursor.execute(sql,val)

conn.commit()

print(cursor.rowcount," record(s) affected")