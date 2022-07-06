from random import random
import sqlite3

def printCourse(course):
    print('-----------------------------------------------------')
    print('Course Name' + ': ' + course[1])
    print('CRN' + ': ' + course[0])
    print('Department' + ': ' + course[2])
    print('Time' + ': ' + course[3])
    print('Days of the Week' + ': ' + course[4])
    print('Semester' + ': ' + course[5])
    print('Year' + ': ' + str(course[6]))
    print('Credits' + ': ' + str(course[7]))
class User:
    def __init__(self, first, last, ID):
        self.first = first
        self.last = last
        self.ID = ID
    def __del__(self):
        pass
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
    # login (I made it global), logout, search, search(parameters)
    def logout(self):
        database.commit()
        del(self)

class Student(User):
    def testS(self):
        print("TestS")
    #add/drop courses
    def addCourseToSemesterSchedule(self, cursor):
        """Allows admins to add a course to the 'SEMESTERSCHEDULE' table. Created by Jacob."""
        if input("Add courses to semester schedule. Hit enter to continue, or type 'exit' to go back: ") == 'exit' : return
        crn = input('CRN: ')
        cursor.execute("SELECT * FROM COURSE WHERE CRN = '%s';" % (crn))
        course = cursor.fetchone()
        if course == None:
            print("Course not found") 
        else:
            # print("""INSERT INTO SEMESTERSCHEDULE VALUES('%s', '%s', '%s');""" % (crn, self.getID(), course[8]))
            try:
                cursor.execute("""INSERT INTO SEMESTERSCHEDULE VALUES('%s', '%s', '%s');""" % (crn, self.getID(), course[8]))
            except:
                print('Course already in semester schedule')

    def dropCourseFromSemesterSchedule(self, cursor):
        """Allows students to drop a course based on a CRN. Created by Jacob"""
        if input("Add courses to semester schedule. Hit enter to continue, or type 'exit' to go back: ") == 'exit' : return
        crn = input('CRN: ')
        cursor.execute("SELECT * FROM COURSE WHERE CRN = '%s';" % (crn))
        course = cursor.fetchone()
        if course == None:
            print("Course not found") 
        else:
            try:
                cursor.execute("""DELETE FROM SEMESTERSCHEDULE WHERE CRN='%s';""" % (crn))
            except:
                print('Course not in semester schedule')


class Instructor(User):
    def testI(self):
        print("TestI")
    #assemble and print course roster
    def instructorPrintSchedule(self, cursor):
        """Prints the schedule of an instructor. Created by Jacob"""
        cursor.execute("""SELECT * FROM COURSE WHERE INSTRUCTORID = '%s';""" % self.getID())
        allClasses = cursor.fetchall()
        if(allClasses.__len__() == 0):
            print("No classes found.")
        else:
            for course in allClasses:
                printCourse(course)

class Admin(User):
    def testA(self):
        print("TestA")
    #create/remove courses

    def createCourse(cursor):
        """Allows admins to add a course to the 'course' table. Created by Tom."""
        while(1):
            if input("Add courses. Hit enter to continue, or type 'exit' to go back: ") == 'exit' : return
            crn = input('CRN: ')
            title = input("Course title: ")
            dept = input("Department (four letter abbr.): ")
            time = input("Meeting time: ") 
            days = input('Meeting days: ')
            semester = input('Semester: ')
            year = input('Year: ')
            credits = input('Credits: ')
            try:
                cursor.execute("""INSERT INTO course VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');""" % (crn, title, dept, time, days, semester, year, credits))
            except:
                print("Error in parameter inputs.")

    def removeCourse(cursor):
        """Allows admins to remove a course from the 'course' table. Created by Tom."""
        while(1):
            if input("Remove courses. Hit enter to continue, or type 'exit' to go back: ") == 'exit' : return
            crn = input("Input the CRN of the course to delete: ")
            try:
                cursor.execute("""SELECT * FROM course WHERE crn = '%s';""" %crn)
                print("Course selected: %s" %cursor.fetchall())
                confirm = input("Confirm deletion? (y/n): ")
                match confirm:
                    case 'y':
                        cursor.execute("""DELETE FROM course WHERE crn = '%s';""" %crn)
                    case _:
                        pass
            except:
                print("Course does not exist.")

def login(cursor):
    """Logs the user in, meaning that an object with their name and ID is created and returned to caller. Created and tested by Tom."""
    while(1):
        in_email = input('Email: ')
        # does in_email exist in db?
        cursor.execute("""SELECT email FROM admin WHERE email = '%s' UNION 
                          SELECT email FROM instructor WHERE email = '%s' UNION 
                          SELECT email FROM student WHERE email = '%s';""" %(in_email, in_email, in_email))
        db_email = cursor.fetchone()
        if db_email == None:
            print("Email not found in database."); continue
        else: 
            break
    while(1):
        cursor.execute("""SELECT 'A' FROM admin WHERE email = '%s' UNION 
                          SELECT 'I' FROM instructor WHERE email = '%s' UNION 
                          SELECT 'S' FROM student WHERE email = '%s';""" %(in_email, in_email, in_email))
        userType = cursor.fetchone()
        in_pass = input('Password: ')
        # if in_password == db_password : login (aka create S/I/A object)
        # get password from table based on user type
        if userType[0] == 'A':
            cursor.execute("SELECT password FROM admin WHERE email = '%s';" %in_email)
            db_pass = cursor.fetchone()
        elif userType[0] == 'I':
            cursor.execute("SELECT password FROM instructor WHERE email = '%s';" %in_email)
            db_pass = cursor.fetchone()
        else:
            cursor.execute("SELECT password FROM student WHERE email = '%s';" %in_email)
            db_pass = cursor.fetchone()

        #check password
        if in_pass == db_pass[0]:
            #MAKE OBJECT
            if userType[0] == 'A':   
                cursor.execute("SELECT name FROM admin WHERE email = '%s';" %in_email)
                first = cursor.fetchone()
                cursor.execute("SELECT surname FROM admin WHERE email = '%s';" %in_email)
                last = cursor.fetchone()
                cursor.execute("SELECT id FROM admin WHERE email = '%s';" %in_email)
                ID = cursor.fetchone()
                user = Admin(first[0], last[0], ID[0])
            elif userType[0] == 'I':
                cursor.execute("SELECT name FROM instructor WHERE email = '%s';" %in_email)
                first = cursor.fetchone()
                cursor.execute("SELECT surname FROM instructor WHERE email = '%s';" %in_email)
                last = cursor.fetchone()
                cursor.execute("SELECT id FROM instructor WHERE email = '%s';" %in_email)
                ID = cursor.fetchone()
                user = Instructor(first[0], last[0], ID[0])
            else:
                cursor.execute("SELECT name FROM student WHERE email = '%s';" %in_email)
                first = cursor.fetchone()
                cursor.execute("SELECT surname FROM student WHERE email = '%s';" %in_email)
                last = cursor.fetchone()
                cursor.execute("SELECT id FROM student WHERE email = '%s';" %in_email)
                ID = cursor.fetchone()
                user = Student(first[0], last[0], ID[0])
            break
        else:
            print('Incorrect password. '); continue
    print("Login successful!")
    return user

def searchAll(cursor):
    """Prints all courses. Created by Tom. NOTE: this function should be included in the "search by parameters" function by leaving all parameters blank."""
    cursor.execute("SELECT * FROM courses;")
    print(cursor.fetchall())     
            
def searchParam(cursor):
    """Allows a user to search based on one parameter. Made by Jacob"""
    print('Params: CRN, TITLE, DEPARTMENT, TIME, DAY, SEMESTER, YEAR, CREDITS, INSTRUCTORID')
    param = input("Enter a parameter: ")
    match param:
        case 'CRN':
            crn = input("Enter a CRN: ")
            cursor.execute("SELECT * FROM COURSE WHERE CRN='%s';" %crn)
            courses = cursor.fetchall()
            for course in courses:
                printCourse(course)
        case 'TITLE':
            title = input("Enter a title: ")
            cursor.execute("SELECT * FROM COURSE WHERE TITLE='%s';" %title)
            courses = cursor.fetchall()
            for course in courses:
                printCourse(course)
        case 'DEPARTMENT':
            department = input("Enter a department: ")
            cursor.execute("SELECT * FROM COURSE WHERE DEPARTMENT='%s';" %department)
            courses = cursor.fetchall()
            for course in courses:
                printCourse(course)
        case 'DAYSOFWEEK':
            daysOfWeek = input("Enter a days of week: ")
            cursor.execute("SELECT * FROM COURSE WHERE DAYSOFWEEK='%s';" %daysOfWeek)
            courses = cursor.fetchall()
            for course in courses:
                printCourse(course)
        case 'SEMESTER':
            semester = input("Enter a semester: ")
            cursor.execute("SELECT * FROM COURSE WHERE SEMESTER='%s';" %semester)
            courses = cursor.fetchall()
            for course in courses:
                printCourse(course)
        case 'YEAR':
            year = input("Enter a year: ")
            cursor.execute("SELECT * FROM COURSE WHERE YEAR='%s';" %year)
            courses = cursor.fetchall()
            for course in courses:
                printCourse(course)
        case 'CREDITS':
            credits = input("Enter a credits: ")
            cursor.execute("SELECT * FROM COURSE WHERE CREDITS='%s';" %credits)
            courses = cursor.fetchall()
            for course in courses:
                printCourse(course)
        case 'INSTRUCTORID':
            instructorID = input("Enter an instructor ID: ")
            cursor.execute("SELECT * FROM COURSE WHERE INSTRUCTORID='%s';" %instructorID)
            courses = cursor.fetchall()
            for course in courses:
                printCourse(course)
        case _:
            print('Not a valid param')
        


## Driver Code
# database file connection 
database = sqlite3.connect("src/assignment5.db") 

# cursor objects are used to traverse, search, grab, etc. information from the database, similar to indices or pointers  
cursor = database.cursor() 

user = login(cursor)
if type(user).__name__ == 'Admin':
    while(1):
        choice = input("""ADMIN MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Add courses to system
        (4) Remove courses from system
        (5) Add user to system
        (6) Remove user from system
        (7) Link user to course
        (8) Remove links
        (9) Log out\n""")
        selection = int(choice)
        match selection:
            case 1:
                searchAll(cursor)
            case 2:
                searchParam(cursor)
            case 3:
                user.createCourse(cursor)
            case 4:
                user.removeCourse(cursor)
            case 5:
                user.addUser(cursor) #TODO
            case 6:
                user.removeUser(cursor) #TODO
            case 7:
                user.linkUser(cursor) #TODO
            case 8:
                user.removeLink(cursor) #TODO
            case 9:
                user.logout(cursor) #TODO
            case default:
                print("Not a valid selection. Use characters '1', '2', etc.")
elif type(user).__name__ == 'Instructor':
    while(1):
        choice = input("""INSTRUCTOR MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Print teaching schedule
        (4) Search other teaching schedules 
        (5) Log out\n""") # Do we need #4? I feel like we should do that one last.
        selection = int(choice)
        match selection:
            case 1:
                searchAll(cursor)
            case 2:
                searchParam(cursor)
            case 3:
                user.instructorPrintSchedule(cursor) 
            case 4:
                pass #TODO
            case 5:
                user.logout(cursor) #TODO
            case default:
                print("Not a valid selection. Use characters '1', '2', etc.")
else:
    while(1):
        choice = input("""STUDENT MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Add courses
        (4) Drop courses
        (5) Print schedule
        (6) Log out\n""")
        selection = int(choice)
        match selection:
            case 1:
                searchAll(cursor)
            case 2:
                searchParam(cursor) 
            case 3:
                user.addCourseToSemesterSchedule(cursor) 
            case 4:
                user.dropCourseFromSemesterSchedule(cursor) 
            case 5:
                user.printSchedule(cursor) #TODO
            case 6:
                user.logout(cursor) #TODO
            case default:
                print("Not a valid selection. Use characters '1', '2', etc.")

# close the connection 
database.close()








### OLD CODE ###
def update(cursor):
    uid = input('Enter the ID of the administrator you want to update: ')
    title = input('New Title: ')
    cursor.execute("""UPDATE ADMIN SET TITLE = '%s' WHERE ADMIN.ID = '%s';""" % (title, uid))

def remove(cursor):
    uid = input('Enter the ID of the user you want to remove: ')
    cursor.execute("""DELETE FROM INSTRUCTOR WHERE ID = '%s';""" % (uid))

def potInt(cursor):
    """'Potential Instructors' - Lists instructors who can teach certain courses"""
    dept = input('Query instructors for which department?\n')
    print("Only those that can teach %s classes:" %dept)
    cursor.execute("""SELECT ID, SURNAME FROM INSTRUCTOR WHERE INSTRUCTOR.DEPT = '%s';""" % (dept))
    query_result = cursor.fetchall()
    if query_result == None:
        print("No instructors available.")
    for i in query_result:
	    print(i)