create table professor
(
    national_code char(10) unique,
    professor_no char(5) primary key,
    name_fa nvarchar(512),
    name_en varchar(512),
    father_name varchar(512),
    birth_date char(10),
    mobile char(11),
    department varchar(512),
    title varchar(512) check (title in ('استاد', 'استادیار','دانش')),
    password varchar(512),
    email varchar(512)
);

update professor
set password = MD5(concat( national_code , upper(left(name_en, 1)) , lower(left(SUBSTRING_INDEX(name_en, ' - ', -1), 1))));

update professor
set email = concat(lower(left(name_en, 1)),'.' , SUBSTRING_INDEX(name_en, ' - ', -1), '@aut.ac.ir');

CREATE PROCEDURE professor_view_students (
	in input_course_id char(8)
	)
begin
		select t.student_no
		from takes t join course c
        where c.course_id = t.course_id and c.course_id = input_course_id;
end;

CREATE PROCEDURE professor_view_quizes (
	in course_id char(8)
	)
begin
		select *
		from quiz q
        where q.course_id = course_id;
end;

CREATE PROCEDURE professor_view_assignment (
	in course_id char(8)
	)
begin
		select *
		from assignment a
        where a.course_id = course_id;
end;


CREATE PROCEDURE professor_view_classes (
	in input_professor_no char(5)
	)
begin
		select *
		from course
        where course.professor_no = input_professor_no;
end;

CREATE PROCEDURE create_quizzes (
	in input_course_id char(8), input_name nvarchar(512), input_start_date timestamp,
	 input_end_date timestamp, input_duration int
	)
begin

        declare count int;
		insert into quiz(course_id, name, start_date, end_date, duration)
		    values (input_course_id,input_name ,input_start_date, input_end_date, input_duration);

		select max(quiz_id) into count from quiz;
		insert into participate(student_no, quiz_id) select student_no,count from takes where takes.course_id = input_course_id;
end;

CREATE PROCEDURE create_assignment (
	in input_course_id char(8), input_name nvarchar(512),
	 input_deadline timestamp
	)
begin

		declare count int;
		insert into assignment(course_id, name, deadline )
		    values (input_course_id, input_name, input_deadline);

		select max(assignment_id) into count from assignment;
		insert into submission(student_no, assignment_id) select student_no,count from takes where takes.course_id = input_course_id;
end;

CREATE PROCEDURE professor_view_answers (in input_quiz_id int)
begin
		select  a.student_no , a.student_input, r.description
		from quiz_answer a join question_quiz q join radio_button r
		where a.question_id = q.question_id and
		      q.quiz_id = input_quiz_id and
		      r.question_id = q.question_id;
end;

CREATE PROCEDURE professor_view_submission (in input_assignment_id int)
begin
		select q.question_id ,a.student_no, a.student_input, sh.description
		from question_assignment q join assignment_answer a join short_answer sh
		where input_assignment_id = q.assignment_id and
		      a.question_id = q.question_id and
		      sh.question_id = q.question_id;
end;

create procedure score_assignment (in input_assignment_id int,in input_student_no char(7),in input_grade numeric(4,2) ,out result int)
begin
    declare temp timestamp;
    set result = 0;
    select a.deadline into temp from assignment as a where a.assignment_id = input_assignment_id;
    if unix_timestamp(current_timestamp()) - unix_timestamp(temp) >= 0 then
        update submission
        set grade = input_grade
        where student_no = input_student_no and
          assignment_id = input_assignment_id;
        set result = 1;
    end if;
end;


