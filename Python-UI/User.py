import sys
import student
import professor


def login_menu(connection):
    login_flag = 0
    while login_flag == 0:
        print("********************")
        print("Please enter your User_id (Enter E or e to exit): ")
        user_id = input()
        if user_id == 'E' or user_id == 'e':
            sys.exit()
        print("Please enter your Password : ")
        password = input()
        user_type = login(connection, user_id, password)
        if user_type == 1 or user_type == 2:
            print("Login successfully")
            login_flag = 1
            if user_type == 1:
                professor.professor_menu(connection, user_id, password)
            if user_type == 2:
                student.student_menu(connection, user_id, password)
        else:
            print("-- Invalid username or password !")


def login(connection, user_id, password):
    myCursor = connection.cursor()
    args = [user_id, password]
    myCursor.callproc('login', args)
    connection.commit()
    user_type = 0
    for result in myCursor.stored_results():
        user_type = result.fetchall()[0][0]
    connection.commit()
    return user_type


def logout(connection, user_id):
    myCursor = connection.cursor()
    args = [user_id]
    myCursor.callproc('logout', args)
    connection.commit()


def change_password(connection, user_id, password, user_type):
    print("Please Enter your old password :")
    old_password = input()
    print("Please Enter your new Password :")
    new_password = input()

    if password == old_password:
        myCursor = connection.cursor()
        res = ''
        args = [user_id, old_password, new_password, res]
        myCursor.callproc('change_password', args)
        connection.commit()
        change_result = 0
        for result in myCursor.stored_results():
            change_result = result.fetchall()[0][0]
        connection.commit()
        if change_result == -1:
            print("-- Password length must be between 8 and 20")
        if change_result == 0:
            print("-- Password must contain letters and numbers")
        if change_result == 1:
            print("-- Password updates successfully")
        if user_type == 1:
            professor.professor_menu(connection, user_id, password)
        if user_type == 2:
            student.student_menu(connection, user_id, password)
    else:
        print("-- Old Password Doesn't match !")
        if user_type == 1:
            professor.professor_menu(connection, user_id, password)
        if user_type == 2:
            student.student_menu(connection, user_id, password)
