import User


def student_menu(connection, user_id, password):
    print("********************")
    print("Hi Student !")
    print("Please Enter one option : ")
    print("1) List of Classes\n2) Change Password\n3) Logout")
    option = int(input())
    print("********************")
    if option == 1:
        get_classes(connection, user_id, password)
    elif option == 2:
        User.change_password(connection, user_id, password, 2)
    elif option == 3:
        User.logout(connection, user_id)
        print("Bye !")
        User.login_menu(connection)
    else:
        print("-- Invalid Option !")
        student_menu(connection, user_id, password)


def get_classes(connection, user_id, password):
    myCursor = connection.cursor()
    args = [user_id]
    myCursor.callproc('student_get_classes', args)
    connection.commit()
    classes = []
    for result in myCursor.stored_results():
        classes = result.fetchall()

    print("Classes : ")
    for i in range(0, len(classes)):
        print(str(i + 1) + ") " + str(classes[i][1]))
    connection.commit()

    print("Please Select a course : ")
    option = int(input())
    if option > len(classes)+1 or option < 0:
        print("-- Invalid option")
        get_classes(connection, user_id, password)
    else:
        course_id = classes[option-1][0]
        print("course_id : ", course_id)
        print("1) list of quizzes\n2) list of assignments\n"
              "3) exit\n")
        option = int(input())
        if option == 1:
            get_course_quizzes(connection, user_id, password, course_id)
        elif option == 2:
            get_course_assignments(connection, user_id, password, course_id)
        elif option == 3:
            student_menu(connection, user_id, password)
        else:
            print("-- Invalid option")


def get_course_quizzes(connection, user_id, password, course_id):
    myCursor = connection.cursor()
    args = [course_id]
    myCursor.callproc('student_view_quizzes', args)
    connection.commit()
    quizzes = []
    for result in myCursor.stored_results():
        quizzes = result.fetchall()
    connection.commit()
    print("Quizzes :")
    for i in range(0, len(quizzes)):
        print(str(i + 1) + ") " + " - id : " + str(quizzes[i][0])
              + ' - name :' + str(quizzes[i][2])
              + ' - start : ' + str(quizzes[i][3])
              + ' - end : ' + str(quizzes[i][4])
              + ' - duration : ' + str(quizzes[i][5]))

    print("Do you want to enter an exam ?(Y/N)")
    option = input()
    if option == 'N':
        student_menu(connection, user_id, password)
    elif option == 'Y':
        print("Enter quiz id :")
        q_id = int(input())
        myCursor = connection.cursor()
        res = ''
        args = [q_id, user_id, res]
        myCursor.callproc('enter_exam', args)
        connection.commit()
        for result in myCursor.stored_results():
            res = result.fetchall()[0][0]
        if res == 1:
            print("-- You have already taken this quiz !")
            student_menu(connection, user_id, password)
        elif res == 2:
            print("-- You can enter exam before start time")
            student_menu(connection, user_id, password)
        elif res == 3:
            print("-- You cannot enter exam after end time")
            student_menu(connection, user_id, password)
        else:
            print("Don't panic, Take a Deep breath :)")
            show_quiz(connection, user_id, password, course_id, q_id)


def show_quiz(connection, user_id, password, course_id, quiz_id):
    myCursor = connection.cursor()
    args = [quiz_id]
    myCursor.callproc('show_quiz_questions', args)
    connection.commit()
    questions = []
    for result in myCursor.stored_results():
        questions = result.fetchall()
    connection.commit()
    print("---------- Quiz #" + str(quiz_id) + ":")
    for i in range(0, len(questions)):
        print("Question #", str(i + 1))
        print('Description : ', str(questions[i][1]))
        print("1)", str(questions[i][2]))
        print("2)", str(questions[i][3]))
        print("3)", str(questions[i][4]))
        print("4)", str(questions[i][5]))
        print("Your Answer :")
        answer = int(input())
        myCursor = connection.cursor()
        res = ''
        args = [quiz_id, questions[i][0], user_id, answer, res]
        myCursor.callproc('submit', args)
        connection.commit()
        for result in myCursor.stored_results():
            res = result.fetchall()[0][0]
        if res == 0:
            myCursor1 = connection.cursor()
            args1 = [user_id, quiz_id, questions[i][0], answer]
            myCursor1.callproc('update_quiz_score', args1)
            connection.commit()
            for result in myCursor1.stored_results():
                result.fetchall()
            connection.commit()
            print("submitted successfully")
        if res == 1:
            print("time is over !")
            student_menu(connection, user_id, password)

    student_menu(connection, user_id, password)


def get_course_assignments(connection, user_id, password, course_id):
    myCursor = connection.cursor()
    args = [course_id]
    myCursor.callproc('student_view_assignment', args)
    connection.commit()
    assignments = []
    for result in myCursor.stored_results():
        assignments = result.fetchall()
    connection.commit()
    print("assignments :")
    for i in range(0, len(assignments)):
        print(str(i + 1) + ") " + " - id : " + str(assignments[i][0])
              + ' - name :' + str(assignments[i][2])
              + ' - deadline : ' + str(assignments[i][3]))

    print("Do you want to enter an assignment ?(Y/N)")
    option = input()
    if option == 'N':
        student_menu(connection, user_id, password)
    elif option == 'Y':
        print("Enter assignment id :")
        a_id = int(input())

        print("assignment_id : ", a_id)
        print("1) list of answers\n2) answer assignment\n"
              "3) exit\n")
        option = int(input())
        if option == 1:
            get_submissions(connection, user_id, password, course_id, a_id)
        if option == 2:
            update_answer(connection, user_id, password, course_id, a_id)
        if option == 3:
            student_menu(connection, user_id, password)


def get_submissions(connection, user_id, password, course_id, a_id):
    myCursor = connection.cursor()
    args = [user_id, a_id]
    myCursor.callproc('student_get_submissions', args)
    connection.commit()
    answers = []
    for result in myCursor.stored_results():
        answers = result.fetchall()
    connection.commit()
    print("answers :")
    for i in range(0, len(answers)):
        print(str(i + 1) + ") " + "id : " + str(answers[i][0])
              + ' - student answer :' + str(answers[i][1])
              + ' - description : ' + str(answers[i][2]))

    student_menu(connection, user_id, password)


def update_answer(connection, user_id, password, course_id, a_id):
    print("Assignment Questions :")
    myCursor = connection.cursor()
    args = [a_id]
    myCursor.callproc('show_assignment_questions', args)
    connection.commit()
    questions = []
    for result in myCursor.stored_results():
        questions = result.fetchall()
    connection.commit()
    print("questions :")
    for i in range(0, len(questions)):
        print(str(i + 1) + ") " + "id : " + str(questions[i][0])
              + ' - description : ' + str(questions[i][1]))

    print("Do you want to answer ?(Y/N)")
    option = input()
    if option == 'N':
        student_menu(connection, user_id, password)
    if option == 'Y':
        print("Enter Question id :")
        q_id = int(input())
        print("Enter Your answer :")
        answer = input()

        myCursor = connection.cursor()
        res = ''
        args = [a_id, q_id, user_id, answer, res]
        myCursor.callproc('student_update_submissions', args)
        connection.commit()
        res = ''
        for result in myCursor.stored_results():
            res = result.fetchall()[0][0]
        connection.commit()
        if res == 0:
            print("Answer updated")
        if res == 1:
            print("time is over!")
        student_menu(connection, user_id, password)
