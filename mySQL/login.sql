create procedure login (in user_id char(7), password varchar(512))
begin
    declare res int;
    if length(user_id) = 5 then
        select 1 into res from professor as p
                              where p.professor_no = user_id
                              and
                              MD5(password) = p.password;
    end if;
    if length(user_id) = 7 then
        select 2 into res from student as t
                              where t.student_no = user_id
                              and
                              MD5(password) = t.password;
    end if;

    if res = 1 then
        insert into professor_log values
        (user_id, current_timestamp());
    end if;

    if res = 2 then
        insert into student_log values
        (user_id, current_timestamp());
    end if;
    select res;
end;

create procedure logout(in user_id char(7))
begin
    delete from student_log where student_no = user_id;
    delete from professor_log where professor_no = user_id;
end;
