create table takes
(
    course_id char(8),
    student_no char(7),
    primary key (student_no, course_id),
    foreign key (student_no) references student(student_no),
    foreign key (course_id) references course(course_id)
);

