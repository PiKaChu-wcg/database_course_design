```maria
use mysql
select user,host from user
CREATE USER root@% IDENTIFIED BY 123456
GRANT ALL PRIVILEGES ON *.* TO root@% WITH GRANT OPTION
FLUSH PRIVILEGES

drop database if exists exam;
create database examl;
```

# 建表,触发器


```maria
create table subject(
s_num varchar(1) PRIMARY KEY,
s_name varchar(5)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table chapter(
c_num char(3) primary key,
c_name char(10),
s_num char(1) ,
FOREIGN KEY(s_num) REFERENCES subject(s_num)
)engine=InnoDB default charset=utf8;

create table question(
q_num int(10) primary key AUTO_INCREMENT,
q_time timestamp default CURRENT_TIMESTAMP,
c_num char(3),
FOREIGN KEY(c_num) REFERENCES chapter(c_num),
q_score int(3),
q_type char (5),
q_content text
)engine=InnoDB default charset=utf8;

create table exam(
e_num nvarchar(10) primary key,
e_time Timestamp default CURRENT_TIMESTAMP,
e_name char(20)
)engine=InnoDB default charset=utf8;

create table content(
e_num nvarchar(10),
FOREIGN KEY(e_num) REFERENCES exam(e_num),
q_num int(10),
FOREIGN KEY(q_num) REFERENCES question(q_num),
PRIMARY KEY (e_num,q_num)
)engine=InnoDB default charset=utf8;

create table teacher(
t_num int(10) primary key AUTO_INCREMENT,
t_name char(4) default ‘匿名’,
s_num varchar(1),
FOREIGN KEY(s_num) REFERENCES subject(s_num)
)engine=InnoDB default charset=utf8;

create table student(
s_num char(10) primary key,
s_name char(4) default ‘匿名’,
t_num int(10),
foreign key(t_num) reference teacher(t_num)
)engine=InnoDB default charset=utf8;

create table test(
s_num char(10),
e_num nvarchar(10),
score int(3) default 60,
primary key (s_num,e_num),
FOREIGN KEY(s_num) REFERENCES student(s_num),
FOREIGN KEY(e_num) REFERENCES exam(e_num),
t_num int(10),
foreign key(t_num) reference teacher(t_num)
)engine=InnoDB default charset=utf8;

DELIMITER //
create trigger question_use_time
after insert on content for each row
begin
update question
set q_use_time=q_use_time+1
where question.q_num = new.q_num;
end//
DELIMITER ;

insert into subject values(‘Y’,‘语文’);
insert into chapter values(‘YGS’,‘赤壁赋’,‘Y’);
insert into question(c_num,q_score,q_type,q_content) values(‘YGS’,10,‘简答’,‘请默写赤壁赋’);
insert into exam(e_name) values(‘期中考’);
insert into content values(1,1);
```

# 存储过程
```maria
create view s_name_q_type
as
select distinct s_name,q_type from subject, chapter, question
where subject.s_num=chapter.s_num and chapter.c_num=question.c_num;

DELIMITER //
create procedure check_type(in s varchar(5))
begin
select q_type as 题型 ,count(*) as 数目 from subject, chapter, question
where subject.s_num=chapter.s_num and chapter.c_num=question.c_num and s_name=s
group by question.q_type;
end//
DELIMITER ;
call check_type(‘语文’);

DELIMITER //
create procedure check_chapter(in s varchar(5))
begin
select c_name as 章节 ,count(*) as 数目 from subject, chapter, question
where subject.s_num=chapter.s_num and chapter.c_num=question.c_num and s_name=s
group by c_name;
end//
DELIMITER ;
call check_chapter(‘语文’);

drop procedure if exists check_subject;
DELIMITER //
create procedure check_subject()
begin
select s_name as 章节 ,count(*) as 数目 from subject, chapter, question
where subject.s_num=chapter.s_num and chapter.c_num=question.c_num
group by s_name;
end//
DELIMITER ;
call check_subject();

drop procedure if exists check_type_num;
DELIMITER //
create procedure check_type_num()
begin
select q_type as 章节 ,count(*) as 数目 from subject, chapter, question
where subject.s_num=chapter.s_num and chapter.c_num=question.c_num
group by q_type;
end//
DELIMITER ;
call check_type_num();
```