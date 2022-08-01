create table student
(
    national_code char(10) unique,
    student_no char(7) primary key,
    name_fa nvarchar(512),
    name_en varchar(512),
    father_name varchar(512),
    birth_date char(10),
    mobile char(11),
    major nvarchar(512),
    password varchar(512),
    email varchar(512)
);


# update password
update student
set password = MD5(concat( national_code , upper(left(name_en, 1)) , lower(left(SUBSTRING_INDEX(name_en, ' - ', -1), 1))));

# update emails
update student
set email = concat(lower(left(name_en, 1)),'.' , SUBSTRING_INDEX(name_en, ' - ', -1), '@aut.ac.ir');


CREATE PROCEDURE student_view_quizzes (in course_id char(8))
begin
		select *
		from quiz q
        where q.course_id = course_id;
end;

CREATE PROCEDURE student_view_assignment (
	in course_id char(8)
	)
begin
		select *
		from assignment a
        where a.course_id = course_id;
end;

CREATE PROCEDURE enter_exam (
	in input_quiz_id int , in input_student_no char(7) , out result int
	)
begin

        declare start timestamp;
        declare end timestamp;

        set result = 0;

		select 1 into result from participate as p where input_quiz_id = p.quiz_id and input_student_no = p.student_no;

        select start_date into start from quiz as q where q.quiz_id = input_quiz_id;
        select end_date into end from quiz as q where q.quiz_id = input_quiz_id;

        if unix_timestamp(current_timestamp()) < unix_timestamp(start) then
            set result = 2;
        end if;

        if unix_timestamp(current_timestamp()) > unix_timestamp(end) then
            set result = 3;
        end if;

        if result = 0 then
            insert into participate(student_no, quiz_id, grade) values (input_student_no,input_quiz_id,null);
        end if;
end;

CREATE PROCEDURE show_quiz (
	in input_quiz_id int
	)
begin
		select r.question_id, r.description, r.option1, r.option2, r.option3, r.option4
		from question_quiz as q , radio_button as r
        where q.quiz_id = input_quiz_id and q.question_id = r.question_id;
end;

CREATE PROCEDURE submit (
	in input_quiz_id int ,in input_question_id int , in input_student_no char(7) , in input_answer int , out result int
	)
begin
        declare end timestamp;
        set result = 0;

        select end_date into end from quiz as q where q.quiz_id = input_quiz_id;
        if unix_timestamp(current_timestamp()) > unix_timestamp(end) then
            set result = 1;
        end if;

        if result = 0 then
            insert into quiz_answer(question_id,student_no,student_input) values (input_question_id,input_student_no,input_answer);
#           call update_quiz_score(input_student_no,input_quiz_id,input_question_id,input_answer);
        end if;
end;

CREATE PROCEDURE check_view_validation (
	in input_quiz_id int, out result int
	)
begin
		declare end timestamp;
        set result = 0;

        select end_date into end from quiz as q where q.quiz_id = input_quiz_id;
        if unix_timestamp(current_timestamp()) > unix_timestamp(end) then
            set result = 1;
        end if;
end;

CREATE PROCEDURE student_get_submissions (
	in input_student_no char(7), in input_assignment_id int)
begin
		select  a.question_id, a.student_input,s.description
        from question_assignment q , assignment_answer as a, short_answer as s
        where q.assignment_id = input_assignment_id
            and q.question_id = a.question_id
		    and a.student_no = input_student_no
		    and s.question_id = q.question_id and s.question_id = a.question_id;

end;

CREATE PROCEDURE student_update_submissions (in input_assignment_id int, in input_question_id int,
	in input_student_no char(7),in input_student_input nvarchar(512), out result int)
begin

		declare exist int default 0;
		declare end timestamp;
		set result = 0;


		select 1 into exist from assignment_answer where student_no = input_student_no and input_question_id = question_id;


        select deadline into end from assignment as q where q.assignment_id = input_assignment_id;
		if unix_timestamp(current_timestamp()) > unix_timestamp(end) then
            set result = 1;
        end if;

		if result = 0 then
            if exist = 0 then

                insert into assignment_answer(question_id, student_no, student_input)
                    values (input_question_id,input_student_no,input_student_input);
            end if;
            if exist = 1 then

                update assignment_answer
                    set student_input = input_student_input
                where question_id = input_question_id and student_no = input_student_no;
            end if;
        end if;
end;

CREATE PROCEDURE student_get_classes (
	in input_student_no char(7))
begin
		select course.course_id , course.course_name
		from takes , course
		where takes.student_no = input_student_no and takes.course_id = course.course_id;
end;

create procedure update_quiz_score(in input_student_no char(7),
 in input_quiz_id int , in input_question_id int ,
 in input_student_answer int)
    begin

        declare c_answer int;

        select correct_answer into c_answer from radio_button
        where radio_button.question_id = input_question_id;

        if c_answer = input_student_answer then
            update participate
            set grade = grade + 1
            where input_student_no = participate.student_no and
                  input_quiz_id = participate.quiz_id;
        end if;
    end;

create procedure show_assignment_questions(in input_assignment_id int)
    begin
        select q.question_id , s.description
        from question_assignment as q, short_answer as s
        where q.question_id = s.question_id and input_assignment_id = q.assignment_id;
    end;

create procedure quiz_review(in input_quiz_id int , in input_student_id char(7))
    begin

        declare result int default 0;
        declare end timestamp;

        select end_date into end from quiz as q where q.quiz_id = input_quiz_id;

		if unix_timestamp(current_timestamp()) > unix_timestamp(end) then
            set result = 1;
        end if;

        if result = 1 then

            select r.description,r.correct_answer,q.student_input
            from radio_button as r,quiz_answer as q , question_quiz as qq
            where qq.question_id = input_quiz_id and q.student_npo = input_student_id
                    and r.question_id =q.question_id;
        end if;
end;

call quiz_review(11,9231010);

create procedure get_score(in input_quiz_id int , in input_student_id char(7))
    begin

        declare result int default 0;
        declare end timestamp;

        select end_date into end from quiz as q where q.quiz_id = input_quiz_id;

		if unix_timestamp(current_timestamp()) > unix_timestamp(end) then
            set result = 1;
        end if;

        if result = 0 then

            select participate.grade
            from participate
            where participate.student_no = input_student_id and participate.quiz_id = input_quiz_id;

        end if;
end;
