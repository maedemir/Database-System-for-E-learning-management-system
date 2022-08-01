CREATE PROCEDURE view_courses (
	in user_id char(8)
	)
	begin
		if length(user_id) = 7 then
		    SELECT course_id  FROM takes WHERE takes.student_no = user_id;
		end if;
		if length(user_id) = 5 then
             SELECT course_id  FROM course WHERE professor_no = user_id;
        end if;
	end;

# call view_courses('31004');
