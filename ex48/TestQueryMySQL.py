import mysql.connector

server = 'localhost'
port = 3306
database = 'studentmanagement'
username = 'root'
password = '@Obama123'

conn = mysql.connector.connect(
    host = server,
    port = port,
    database = database,
    user = username,
    password = password
)

cursor = conn.cursor()

sql="select * from student"
cursor.execute(sql)
print('Dataset:')

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()

print('-'*50)

cursor = conn.cursor()
sql = 'select * from student where Age >= 22 and Age <= 26'
cursor.execute(sql)
print('Students age between 22 and 26:')

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()

print('-'*50)

cursor = conn.cursor()
sql = 'select * from student order by Age asc'
cursor.execute(sql)
print('Students ordered by age ascending:')

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()

print('-'*50)

cursor = conn.cursor()
sql = ('select * from student where Age>= 22 and Age <= 26 '
       'order by Age desc')
cursor.execute(sql)
print('Students age between 22 and 26 ordered by age descending:')

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()

print('-'*50)

cursor = conn.cursor()
sql = 'select * from student where ID=1'
cursor.execute(sql)
print('Student with ID=1:')

dataset = cursor.fetchone()
if dataset != None:
    id, code, name, age, avatar, intro = dataset
    print('ID =', id)
    print('Code =', code)
    print('Name =', name)
    print('Age =', age)

cursor.close()

print('-'*50)

cursor = conn.cursor()
sql = 'select * from student LIMIT 3 OFFSET 0'
cursor.execute(sql)
print('First 3 students:')

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()

print('-'*50)

cursor = conn.cursor()
sql = 'select * from student LIMIT 3 OFFSET 3'
cursor.execute(sql)
print('Next 3 students:')

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()

print('-'*50)

print("PAGING!?")
cursor = conn.cursor()
sql="select count(*) from student"
cursor.execute(sql)
dataset=cursor.fetchone()
rowcount=dataset[0]

limit=3
step=3
for offset in range(0,rowcount,step):
    sql=f"select * from student LIMIT {limit} OFFSET {offset}"
    cursor.execute(sql)

    dataset=cursor.fetchall()
    align='{0:<3} {1:<6} {2:<15} {3:<10}'
    print(align.format('ID', 'Code','Name',"Age"))
    for item in dataset:
        id=item[0]
        code=item[1]
        name=item[2]
        age=item[3]
        avatar=item[4]
        intro=item[5]
        print(align.format(id,code,name,age))

cursor.close()

print('-'*50)

cursor = conn.cursor()
sql = 'insert into student (code, name, age) values (%s, %s, %s)'
val = ('sv07', 'Tran Duy Thanh', 45)
cursor.execute(sql, val)

conn.commit()
print(cursor.rowcount, 'record inserted')

cursor.close()

print('-'*50)

cursor = conn.cursor()
sql = 'insert into student (code, name, age) values (%s, %s, %s)'
val = [
    ('sv08', 'Putin', 19),
    ('sv09', 'Biden', 22),
    ('sv10', 'Trump', 25)
]

cursor.executemany(sql, val)

conn.commit()
print(cursor.rowcount, 'records inserted')

cursor.close()