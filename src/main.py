from random import random
from collections import Counter
import sqlite3


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
    def logout(self):
        database.commit()
        del(self)

class Student(User):
    def addCourseToSemesterSchedule(self, cursor):
        """Allows students to add a course to the 'SEMESTERSCHEDULE' table. Created by Jacob."""
        if input("Add courses to semester schedule. Hit enter to continue, or type 'exit' to go back: ") == 'exit' : return
        crn = input('CRN: ')
        cursor.execute("SELECT * FROM COURSE WHERE CRN = '%s';" % (crn))
        course = cursor.fetchone()
        if course == None:
            print("Course not found") 
        else:
            try:
                cursor.execute("""INSERT INTO SEMESTERSCHEDULE VALUES('%s', '%s', '%s');""" % (crn, self.getID(), course[8]))
            except:
                print('Course already in semester schedule')

    def studentPrintSchedule(self, cursor):
        """Prints the schedule of an student. Created by Tom."""
        cursor.execute("""SELECT CRN FROM SEMESTERSCHEDULE WHERE STUDENTID = '%s';""" % self.getID())
        allCRNs = cursor.fetchone()
        if(allCRNs.__len__() == 0):
            print("No classes found.")
        else:
            for crn in allCRNs:
                cursor.execute("SELECT * FROM COURSE WHERE CRN='%s';" %crn)
                course = cursor.fetchone()
                printCourse(course)

    def checkConflicts(self, cursor):
        """Checks if the student has conflicting class times. Created by Tom."""
        #get list of CRNs
        cursor.execute("""SELECT CRN FROM SEMESTERSCHEDULE WHERE STUDENTID = '%s';""" % self.getID())
        allCRNs = cursor.fetchall()
        if(allCRNs.__len__() == 0):
            print("No classes found.")
        else:
            times = []
            days = []
            #make two lists for storing each class's meeting time and days
            for crn in allCRNs:
                cursor.execute("SELECT TIME FROM COURSE WHERE CRN='%s';" %crn)
                time = cursor.fetchone()
                times.append(time)
                cursor.execute("SELECT DAYSOFWEEK FROM COURSE WHERE CRN='%s';" %crn)
                day = cursor.fetchone()
                days.append(day)
            #check for common days
            i = 0
            while i < len(days)-1:
                j = i+1
                while j <= len(days)-1:
                    if(isCommon(days[i], days[j]) == 1):
                        #check times
                        if (times[i] == times[j]):
                            print("Conflicting CRNs: %s, %s" % (allCRNs[i][0], allCRNs[j][0]))
                            #print(','.join([str(j[0]) for j in allCRNs])
                            return
                    j += 1
                i += 1
            print("No conflicts!")

    def dropCourseFromSemesterSchedule(self, cursor):
        """Allows students to drop a course based on a CRN. Created by Jacob."""
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
    def createCourse(self, cursor):
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
                cursor.execute("""INSERT INTO course VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 0);""" % (crn, title, dept, time, days, semester, year, credits)) ##table has a new column!!!!!!!!!!
            except:
                print("Error in parameter inputs.")

    def removeCourse(self, cursor):
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
            print('Incorrect password.'); continue
    print("Login successful!")
    return user

def isCommon(str1,str2):  # taken from https://www.geeksforgeeks.org/python-code-print-common-characters-two-strings-alphabetical-order/
    # convert both strings into counter dictionary
    dict1 = Counter(str1)
    dict2 = Counter(str2)
    # take intersection of these dictionaries
    commonDict = dict1 & dict2
    if len(commonDict) == 0:
        return 0 #FALSE
    else:
        return 1 #TRUE

def printCourse(course):
    print('-------------------------------------------')
    print('Course Name' + ': ' + course[1])
    print('CRN' + ': ' + course[0])
    print('Department' + ': ' + course[2])
    print('Time' + ': ' + course[3])
    print('Days of the Week' + ': ' + course[4])
    print('Semester' + ': ' + course[5])
    print('Year' + ': ' + str(course[6]))
    print('Credits' + ': ' + str(course[7]))

def searchAll(cursor):
    """Prints all courses. Created by Tom."""
    cursor.execute("SELECT * FROM course;")
    courses = cursor.fetchall()
    for course in courses:
        printCourse(course)     
            
def searchParam(cursor):
    """Allows a user to search based on one parameter. Made by Jacob"""
    print('Params: CRN, TITLE, DEPARTMENT, TIME, DAYS, SEMESTER, YEAR, CREDITS, INSTRUCTORID')      #There is no case statement for 'Time'
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
        case 'DAYS':
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
database = sqlite3.connect("src/main.db") 

# cursor objects are used to traverse, search, grab, etc. information from the database, similar to indices or pointers  
cursor = database.cursor() 

user = login(cursor)
if type(user).__name__ == 'Admin':
    while(1):
        choice = input("""\nADMIN MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Add courses to system
        (4) Remove courses from system
        (5) Add user to system
        (6) Remove user from system
        (7) Link user to course
        (8) Remove links
        (9) Save and log out\n""")
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
                user.logout()
                break
            case _:
                print("Not a valid selection. Use characters '1', '2', etc.")
elif type(user).__name__ == 'Instructor':
    while(1):
        choice = input("""\nINSTRUCTOR MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Print teaching schedule
        (4) Search other teaching schedules 
        (5) Save and log out\n""") # Do we need #4? I feel like we should do that one last.
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
                user.logout()
                break
            case _:
                print("Not a valid selection. Use characters '1', '2', etc.")
else:
    while(1):
        choice = input("""\nSTUDENT MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Add courses
        (4) Drop courses
        (5) Print schedule
        (6) Check for schedule conflicts
        (7) Save and log out\n""")
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
                user.studentPrintSchedule(cursor)
            case 6:
                user.checkConflicts(cursor)
            case 7:
                user.logout()
                break
            case _:
                print("Not a valid selection. Use characters '1', '2', etc.")

# close the connection 
database.close()