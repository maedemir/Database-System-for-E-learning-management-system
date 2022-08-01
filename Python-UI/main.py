import User
import mysql.connector
from mysql.connector import Error

'''
student_user_test = "9212001" 9231026
student_pass_test = "2744740129Me" 3130293946Hm

professor_user_test = "31004"
professor_pass_test = "6825225184Hb"

example of time : 2022-08-01 18:40:30
'''

if __name__ == "__main__":
    try:
        connection = mysql.connector.connect(host='localhost', database='db_project', user='root')
        if connection.is_connected():
            print("connected tos database successfully")
            print("Welcome :D")
            User.login_menu(connection)

    except Error as error:
        print('-- Cannot communicate with Database! ** error : ', error)
        print('For Security reasons you will back to login page :(')
        User.login_menu(connection)
