create procedure change_password (in user_id char(7), old_password varchar(512),new_password varchar(512) ,
out result integer)
begin
    set result = 0;
    if length(new_password) < 8  then
      set result = -1;
    end if;
    if length(new_password) > 20  then
       set result = -1;
    end if;

    if result != -1 then
        if new_password REGEXP '[0-9]' and ( new_password REGEXP '[a-z]'
                or new_password REGEXP '[A-Z]') then
            set result = 1;
        end if;
    end if;

    if result = 1 then
         if length(user_id) = 5 then
        update professor
            set password = MD5(new_password)
        where password = MD5(old_password) and user_id = professor_no;
        end if;
        if length(user_id) = 7 then
            update student
                set password = MD5(new_password)
            where password = MD5(old_password) and user_id = student_no;
        end if;
    end if;

    select result;
end;