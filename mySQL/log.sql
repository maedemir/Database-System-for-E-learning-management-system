create table student_log
(
    student_no char(7) primary key,
    entrance_date timestamp,
    foreign key (student_no) references student(student_no)
);


create table professor_log
(
    professor_no char(5) primary key,
    entrance_date timestamp,
    foreign key (professor_no) references professor(professor_no)
);
