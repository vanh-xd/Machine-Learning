SELECT * FROM student;
SELECT * FROM student where Age >= 22 and Age <= 26;
SELECT * FROM student 
order by Age asc;
SELECT * FROM student 
where Age >= 22 and Age <=26
order by Age desc;

update student
set Name='Obama'
where ID=6;
delete from student where Code='sv06'