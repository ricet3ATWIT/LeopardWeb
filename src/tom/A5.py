import sqlite3

class User:
    def __init__(self, first, last, ID):
        self.first = first
        self.last = last
        self.ID = ID
    def getFirst(self):
        return self.first
    def getLast(self):
        return self.last
    def getID(self):
        return self.ID
    def setFirst(self, first):
        self.first = first
    def setLast(self, last):
       self.last = last
    def setID(self, ID):
       self.ID = ID
    def printAll(self):
        print("First: ", self.first)
        print("Last: ", self.last)
        print("ID: ", self.ID)

class Student(User):
    def testS(self):
        print("TestS")

class Instructor(User):
    def testI(self):
        print("TestI")

class Admin(User):
    def testA(self):
        print("TestA")

## SQL
# database file connection 
database = sqlite3.connect("src/assignment5.db") 
  
# cursor objects are used to traverse, search, grab, etc. information from the database, similar to indices or pointers  
cursor = database.cursor() 

def searchDB(cursor):
    sql_command = input('Type out your SQL command FULLY:\n')
    cursor.execute(sql_command)
    query_result = cursor.fetchall()
    for i in query_result:
        print(i)

def printDB(cursor):
    """Prints every row from every table in the database."""
    cursor.execute("""SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';""")  #this line taken from: https://www.sqlitetutorial.net/sqlite-show-tables/
    tables = cursor.fetchall()                                                                              #the rest is my code
    for i in tables:
        sql_command = """SELECT * FROM %s;""" %i
        cursor.execute(sql_command)
        query_result = cursor.fetchall()
        for i in query_result:
            print(i)
    
def createTable(cursor):
    print('Type out your SQL command FULLY:\n')  #there has to be an easier way to allow the user to create a table...
    #sql_command = input('')
    sql_command = """CREATE TABLE COURSE (  
    CRN INT PRIMARY KEY NOT NULL,
    TITLE TEXT NOT NULL,
    DEPT CHAR(4) NOT NULL,
    MEET_TIME TEXT,
    DAYS TEXT,
    SEMESTER TEXT,
    YEAR INT,
    CREDITS INT);"""
    cursor.execute(sql_command)

def insert(cursor):
    uid = input('ID: ')
    fname = input("First name: ")
    lname = input("Last name: ")
    gradyear = input("Graduation year: ") 
    major = input('Major (four letter abbr.): ')
    email = input('Email (with no "@wit.edu"): ')
    cursor.execute("""INSERT INTO STUDENT VALUES('%s', '%s', '%s', '%s', '%s', '%s');""" % (uid, fname, lname, gradyear, major, email))

def update(cursor):
    uid = input('Enter the ID of the administrator you want to update: ')
    title = input('New Title: ')
    cursor.execute("""UPDATE ADMIN SET TITLE = '%s' WHERE ADMIN.ID = '%s';""" % (title, uid))

def remove(cursor):
    uid = input('Enter the ID of the user you want to remove: ')
    cursor.execute("""DELETE FROM INSTRUCTOR WHERE ID = '%s';""" % (uid))

def insert2(cursor):
    crn = input('CRN: ')
    title = input("Course title: ")
    dept = input("Departement (four letter abbr.): ")
    time = input("Meeting time: ") 
    days = input('Meeting days: ')
    semester = input('Semester: ')
    year = input('Year: ')
    credits = input('Credits: ')
    cursor.execute("""INSERT INTO COURSE VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');""" % (crn, title, dept, time, days, semester, year, credits))

def potInt(cursor):
    """'Potential Instructors' - Lists instructors who can teach certain courses"""
    dept = input('Query instructors for which department?\n')
    print("Only those that can teach %s classes:" %dept)
    cursor.execute("""SELECT ID, SURNAME FROM INSTRUCTOR WHERE INSTRUCTOR.DEPT = '%s';""" % (dept))
    query_result = cursor.fetchall()
    if query_result == []:
        print("No instructors available.")
    for i in query_result:
	    print(i)

while(1):
    choice = input("""MENU:
    (1) Search database
    (2) Print entire database
    (3) Create (course) table
    (4) Insert (student) tuples
    (5) Update (admin) tuples
    (6) Remove tuples
    (7) Insert (course) tuples
    (8) Potential Intructor Query
    (9) Exit the program\n""")
    selection = int(choice)
    match selection:
        case 1:
            searchDB(cursor)
        case 2:
            printDB(cursor)
        case 3:
            createTable(cursor)
        case 4:
            insert(cursor)
        case 5:
            update(cursor)
        case 6:
            remove(cursor)
        case 7:
            insert2(cursor)
        case 8:
            potInt(cursor)
        case 9:
            break
        case default:
            print("Not a valid selection. Use characters '1', '2', etc.")

# To save the changes in the files. Never skip this.  
# If we skip this, nothing will be saved in the database. 
database.commit() 
  
# close the connection 
database.close()



