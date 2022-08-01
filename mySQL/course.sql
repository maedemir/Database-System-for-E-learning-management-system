create table course
(
    course_id char(8) primary key ,
    course_name nvarchar(512),
    professor_no char(5),
    foreign key (professor_no) references professor(professor_no)
);
