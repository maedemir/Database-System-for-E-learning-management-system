create table quiz
(
    quiz_id int primary key auto_increment,
    course_id char(8),
    name nvarchar(512),
    start_date timestamp,
    end_date timestamp,
    duration integer,
    finished int(1) default 0,
    foreign key (course_id) references course(course_id)
);

create table radio_button
(
     question_id int primary key auto_increment,
     description nvarchar(512),
     option1 nvarchar(512),
     option2 nvarchar(512),
     option3 nvarchar(512),
     option4 nvarchar(512),
     correct_answer int
);

create table quiz_answer
(
     question_id int,
     student_no char(7),
     student_input int,
     primary key (question_id, student_no),
     foreign key (question_id) references radio_button(question_id),
     foreign key (student_no) references student(student_no)
);

create table participate
(
     student_no char(7),
     quiz_id int,
     grade numeric(4,2) default 0.0,
     primary key (student_no, quiz_id),
     foreign key (student_no) references student(student_no),
     foreign key (quiz_id) references quiz(quiz_id)
);

create table question_quiz
(
    quiz_id int,
    question_id int,
    primary key (quiz_id, question_id),
    foreign key (question_id) references radio_button(question_id),
    foreign key (quiz_id) references quiz(quiz_id)
);


create table short_answer
(
    question_id int primary key auto_increment,
    description nvarchar(512),
    correct_answer nvarchar(512)
);

create table assignment
(
    assignment_id int primary key auto_increment,
    course_id char(8),
    name nvarchar(512),
    deadline timestamp,
    foreign key (course_id) references course(course_id)

);

create table assignment_answer
(
     question_id int,
     student_no char(7),
     student_input varchar(512),
     primary key (question_id, student_no),
     foreign key (question_id) references short_answer(question_id),
     foreign key (student_no) references student(student_no)
);

create table submission
(
     student_no char(7),
     assignment_id int,
     grade numeric(4,2),
     primary key (student_no, assignment_id),
     foreign key (student_no) references student(student_no),
     foreign key (assignment_id) references assignment(assignment_id)
);


create table question_assignment
(
    assignment_id int,
    question_id int,
    primary key (assignment_id, question_id),
    foreign key (question_id) references short_answer(question_id),
    foreign key (assignment_id) references assignment(assignment_id)
);

CREATE PROCEDURE add_new_radio_button_question (
	in input_quiz_id int, in input_description nvarchar(512),
	in input_option1 nvarchar(512), in input_option2 nvarchar(512),
	in input_option3 nvarchar(512), in input_option4 nvarchar(512),
	in input_correct_answer nvarchar(512))
begin

        declare id int default 0;

		insert into radio_button(description, option1, option2, option3, option4, correct_answer)
		    values (input_description,input_option1,
		            input_option2,input_option3,input_option4,
		            input_correct_answer);

        select max(question_id) into id from radio_button;

		insert into question_quiz(quiz_id, question_id)
		    values (input_quiz_id,id);

end;


CREATE PROCEDURE add_new_short_answer_question (
	in input_assignment_id int, in input_description nvarchar(512),
	in input_correct_answer nvarchar(512))
begin

        declare id int default 0;

		insert into short_answer(description,correct_answer)
		    values (input_description,input_correct_answer);

        select max(question_id) into id from short_answer;

		insert into question_assignment(assignment_id, question_id)
		    values (input_assignment_id,id);

end;
