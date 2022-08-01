# Database-System-for-E-learning-management-system
This project is an implementation of a database system for university E-learning management system using MySQL and Python
The purpose of this project is to implement the database model using entity-relation model and to directly work with SQL and also is to implement the relationships and work with the implemented model from a separate user interface. 
## Entities
- Student
  * student can : 
    - Login
    - Logout
    - Change his/her password
    - View list of his/her courses
    - View his/her quizzes
    - Enter an exam in right time and answer to that
    - View list of his/her assignment and submit an answer to each one before its deadline
    - View his/her submissions for an assignmemnt
    - Submit an answer for an assignment
    - Update his/her answer for an specified assignment
    - Review a quiz after its deadline
- Professor
  * Professor can : 
    - Login
    - Logout
    - Change his/her password
    - View list of students for each of his/her courses
    - View list of his/her quizzes
    - View list of his/her assignments
    - Create new exam
    - Create new assignment
    - View list of submissions for each assignment
    - View list of answers for each quiz
    - Score each of the submissions for an assignmentض
- Course
- Quiz
- Radio button question (it is used only in quizzes)
- Assignment
- Short answer question (it is used only in assignments)
## Relations 
- quiz_answer --> Shows each student's answer for each quiz question
- participate --> Shows which student has participation in which quiz
- question_quiz --> Shows which radio button question is used in which quiz
- assignment_answer --> Shows each student's answer for each  assignment question
- submission --> Shows relation between student and assignment with their total grade
- question_assignment -->  Shows which short answer question is used in which assignment

# UI 
To access the database for reading and manapulating data, we need a UI.  To meet this need, I simply made a MySQL connenction in python and user commands are entered through python CLI(A simple but useful way to work with our database)
# How to run this project
1. create a database
2. add sql files to yout database project and create tables 
3. using FinalPrjData.xslx, fill the correspondent tables 
4. Add some arbitrary data to the empty tables(Remember to fill out those who are foreign key for other tables)
5. Using python UI you can simply connect your database to UI
6. Done. easy-peasy🤏🏻
