import User


def professor_menu(connection, user_id, password):
    print("********************")
    print("Hi Professor !")
    print("Please Enter one option : ")
    print("1) List of Classes\n2) Change Password\n3) Logout")
    option = int(input())
    print("********************")
    if option == 1:
        get_classes(connection, user_id, password)
    elif option == 2:
        User.change_password(connection, user_id, password, 1)
    elif option == 3:
        User.logout(connection, user_id)
        print("Bye !")
        User.login_menu(connection)
    else:
        print("-- Invalid Option !")
        professor_menu(connection, user_id, password)


def get_classes(connection, user_id, password):
    myCursor = connection.cursor()
    args = [user_id]
    myCursor.callproc('professor_view_classes', args)
    connection.commit()
    classes = []
    for result in myCursor.stored_results():
        classes = result.fetchall()
    print("Classes : ")
    for i in range(0, len(classes)):
        print(str(i + 1) + ") " + classes[i][1])
    connection.commit()
    print("Please select a course: ")
    option = int(input())
    if option > len(classes)+1 or option < 0:
        print("-- Invalid option")
        get_classes(connection, user_id, password)
    else:
        course_id = classes[option-1][0]
        print("course_id : ", course_id)
        print("1) list of students\n2) list of quizzes\n"
              "3) list of assignments\n4) create new quiz\n"
              "5) create new assignment\n"
              "6) add question to quiz\n"
              "7) add question to assignment\n"
              "8) exit\n")

        option = int(input())
        if option == 1:
            get_list_of_students(connection, course_id, user_id, password)
        elif option == 2:
            get_list_of_quizzes(connection, course_id, user_id, password)
        elif option == 3:
            get_list_of_assignments(connection, course_id, user_id, password)
        elif option == 4:
            create_new_quiz(connection, course_id, user_id, password)
        elif option == 5:
            create_new_assignment(connection, course_id, user_id, password)
        elif option == 6:
            add_question_to_quiz(connection, course_id, user_id, password)
        elif option == 7:
            add_question_to_assignment(connection, course_id, user_id, password)
        elif option == 8:
            professor_menu(connection, user_id, password)
        else:
            print("-- Invalid option")


def get_list_of_students(connection, course_id, user_id, password):
    myCursor = connection.cursor()
    args = [course_id]
    myCursor.callproc('professor_view_students', args)
    connection.commit()
    students = []
    for result in myCursor.stored_results():
        students = result.fetchall()
    connection.commit()
    print("Students :")
    for i in range(0, len(students)):
        print(str(i + 1) + ") " + students[i][0])
    professor_menu(connection, user_id, password)


def get_list_of_quizzes(connection, course_id, user_id, password):
    myCursor = connection.cursor()
    args = [course_id]
    myCursor.callproc('professor_view_quizzes', args)
    connection.commit()
    quizzes = []
    for result in myCursor.stored_results():
        quizzes = result.fetchall()
    connection.commit()
    print("Quizzes :")
    for i in range(0, len(quizzes)):
        print(str(i + 1) + ") " + str(quizzes[i][2]) + " - id : " + str(quizzes[i][0]))

    print("Do you want to see answers?(Y/N)")
    option = input()
    if option == 'N':
        professor_menu(connection, user_id, password)
    if option == 'Y':
        print("Enter Quiz id :")
        q_id = int(input())
        myCursor = connection.cursor()
        args = [q_id]
        myCursor.callproc('professor_view_answers', args)
        connection.commit()
        answers = []
        for result in myCursor.stored_results():
            answers = result.fetchall()
        connection.commit()
        print("answers (student_id / answer / description) :")
        for i in range(0, len(answers)):
            print(str(i + 1) + ") " + str(answers[i][0]) + " - " + str(answers[i][1]) + " - " + str(answers[i][2]))
        professor_menu(connection, user_id, password)


def get_list_of_assignments(connection, course_id, user_id, password):
    myCursor = connection.cursor()
    args = [course_id]
    myCursor.callproc('professor_view_assignment', args)
    connection.commit()
    assignments = []
    for result in myCursor.stored_results():
        assignments = result.fetchall()
    connection.commit()
    print("Assignments :")
    for i in range(0, len(assignments)):
        print(str(i + 1) + ") " + str(assignments[i][2]) + " - id : " + str(assignments[i][0]))
    print("Do you want to see answers?(Y/N)")
    option = input()
    if option == 'N':
        professor_menu(connection, user_id, password)
    if option == 'Y':
        print("Enter Assignment id :")
        a_id = int(input())
        myCursor = connection.cursor()
        args = [a_id]
        myCursor.callproc('professor_view_submission', args)
        connection.commit()
        answers = []
        for result in myCursor.stored_results():
            answers = result.fetchall()
        connection.commit()
        print("answers (student_id / answer / description) :")
        for i in range(0, len(answers)):
            print(str(i + 1) + ") " + str(answers[i][1]) + " - " + str(answers[i][2]) + " - " + str(answers[i][3]))

    print("Do you want to set grades?(Y/N)")
    option = input()
    if option == 'N':
        professor_menu(connection, user_id, password)
    if option == 'Y':
        print("Enter assignment_id : ")
        a_id = int(input())
        print("Enter student_id : ")
        s_id = int(input())
        print("Enter grade : ")
        grade = int(input())
        myCursor = connection.cursor()
        res = ''
        args = [a_id, s_id, grade, res]
        myCursor.callproc('score_assignment', args)
        connection.commit()
        for result in myCursor.stored_results():
            res = result.fetchall()[0][0]
        if res == 0:
            print("-- You can set grades after deadline !")
            get_list_of_assignments(connection, course_id, user_id, password)
        else:
            for result in myCursor.stored_results():
                result.fetchall()
            connection.commit()
            print("Grade inserted successfully")
            get_list_of_assignments(connection, course_id, user_id, password)


def create_new_quiz(connection, course_id, user_id, password):
    print("Enter a name for quiz:")
    q_name = input()
    print("Enter a start date (like YYY-MM-DD HH:MM:SS) :")
    start_date = input()
    print("Enter a end date (like YYY-MM-DD HH:MM:SS) :")
    end_date = input()
    print("Enter duration:")
    duration = int(input())
    myCursor = connection.cursor()
    args = [course_id, q_name, start_date, end_date, duration]
    myCursor.callproc('create_quizzes', args)
    connection.commit()
    for result in myCursor.stored_results():
        result.fetchall()
    connection.commit()
    print('Created successfully')
    professor_menu(connection, user_id, password)


def create_new_assignment(connection, course_id, user_id, password):
    print("Enter a name for assignment:")
    a_name = input()
    print("Enter a deadline (like YYY-MM-DD HH:MM:SS) :")
    deadline = input()
    myCursor = connection.cursor()
    args = [course_id, a_name, deadline]
    myCursor.callproc('create_assignment', args)
    connection.commit()
    for result in myCursor.stored_results():
        result.fetchall()
    connection.commit()
    print('Added successfully')
    professor_menu(connection, user_id, password)


def add_question_to_quiz(connection, course_id, user_id, password):
    while 1:
        print("Do you want to add new question ?(Y / N)")
        option = input()
        if option == "N":
            break
        if option == "Y":
            print("Enter Quiz_id:")
            q_id = int(input())
            print("Enter Description:")
            description = input()
            print("Enter option1:")
            option1 = input()
            print("Enter option2:")
            option2 = input()
            print("Enter option3:")
            option3 = input()
            print("Enter option4:")
            option4 = input()
            print("Enter correct answer:")
            correct_answer = int(input())
            myCursor = connection.cursor()
            args = [q_id, description, option1, option2, option3, option4, correct_answer]
            myCursor.callproc('add_new_four_option_question', args)
            connection.commit()
            for result in myCursor.stored_results():
                result.fetchall()
            connection.commit()
            print('Created successfully')

    professor_menu(connection, user_id, password)


def add_question_to_assignment(connection, course_id, user_id, password):
    while 1:
        print("Do you want to add new question ?(Y / N)")
        option = input()
        if option == "N":
            break
        if option == "Y":
            print("Enter assignment_id:")
            a_id = int(input())
            print("Enter Description:")
            description = input()
            print("Enter correct answer:")
            correct_answer = input()
            myCursor = connection.cursor()
            args = [a_id, description, correct_answer]
            myCursor.callproc('add_new_short_answer_question', args)
            connection.commit()
            for result in myCursor.stored_results():
                result.fetchall()
            connection.commit()
            print('Added successfully')

    professor_menu(connection, user_id, password)
