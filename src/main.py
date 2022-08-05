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
                database.commit()
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
                database.commit()
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

    def searchRosters(self, cursor):
      """Allows instructors to search and print course rosters. Created by Tom."""
      while(1):
          if input("Search courses. Hit enter to continue, or type 'exit' to go back: ") == 'exit' : return
          crn = input('Enter a CRN: ')
          try:
              cursor.execute("SELECT STUDENTID FROM SEMESTERSCHEDULE WHERE CRN='%s';" %crn)
              students = cursor.fetchall()
              for kid in students:
                  cursor.execute("SELECT SURNAME, NAME FROM STUDENT WHERE ID='%s';" %kid)
                  student = cursor.fetchall()
                  for i in student:
                      print(i)
          except:
              print("Error in parameter inputs.")

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
            instructorId = input('Instructor Id: ')
            try:
                cursor.execute("""INSERT INTO course VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');""" % (crn, title, dept, time, days, semester, year, credits, instructorId)) 
                database.commit()
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
                        database.commit()
                    case _:
                        pass
            except:
                print("Course does not exist.")

    def createUser(self, cursor):
      print('You can create a student or instructor. Type "student" or "instructor"')
      userType = input('Would you like to create an instructor or student? ')
      if(userType == 'student'):
        self.createStudent(cursor)
      elif(userType == 'instructor'):
        self.createInstructor(cursor)
      else:
        print('Invalid input')
        return
    
    def createStudent(self, cursor):
        """Allows admins to add a student to the 'student' table. Created by Jacob."""
        while(1):
            if input("Add students. Hit enter to continue, or type 'exit' to go back: ") == 'exit' : return
            id = input('ID: ')
            first = input("First name: ")
            surname = input("Surname: ")
            gradYear = input("Graduation year: ")
            major = input("Major: ")
            email = input("Email: ")
            password = input("Password: ")

            try:
                cursor.execute("""INSERT INTO student VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s');""" % (id, first, surname, gradYear, major, email, password)) 
                database.commit()
            except:
                print("Error in parameter inputs.")
    
    
    def createInstructor(self, cursor):
        """Allows admins to add a instructor to the 'instructor' table. Created by Jacob."""
        while(1):
            if input("Add instructors. Hit enter to continue, or type 'exit' to go back: ") == 'exit' : return
            id = input('ID: ')
            first = input("First name: ")
            surname = input("Surname: ")
            title = input("Title: ")
            hireYear = input("Hire year: ")
            dept = input("Department: ")
            email = input("Email: ")
            password = input("Password: ")

            # try:
            cursor.execute("""INSERT INTO instructor VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');""" % (id, first, surname, title, hireYear, dept, email, password)) 
            database.commit()
            # except:
            #     print("Error in parameter inputs.")

    def removeStudent(self, cursor):
        """Allows admins to remove a student from the 'student' table. Created by Jacob."""
        while(1):
            if input("Remove students. Hit enter to continue, or type 'exit' to go back: ") == 'exit' : return
            id = input("Input the ID of the student to delete: ")
            try:
                cursor.execute("""SELECT * FROM student WHERE id = '%s';""" %id)
                print("Student selected: %s" %cursor.fetchall())
                confirm = input("Confirm deletion? (y/n): ")
                match confirm:
                    case 'y':
                        cursor.execute("""DELETE FROM student WHERE id = '%s';""" %id)
                        database.commit()
                    case _:
                        pass
            except:
                print("Student does not exist.")
    
    def removeInstructor(self, cursor):
        """Allows admins to remove a instructor from the 'instructor' table. Created by Jacob."""
        while(1):
            if input("Remove instructors. Hit enter to continue, or type 'exit' to go back: ") == 'exit' : return
            id = input("Input the ID of the instructor to delete: ")
            try:
                cursor.execute("""SELECT * FROM instructor WHERE id = '%s';""" %id)
                print("Instructor selected: %s" %cursor.fetchall())
                confirm = input("Confirm deletion? (y/n): ")
                match confirm:
                    case 'y':
                        cursor.execute("""DELETE FROM instructor WHERE id = '%s';""" %id)
                        database.commit()
                    case _:
                        pass
            except:
                print("Instructor does not exist.")

    def removeUser(self, cursor):
        """Allows admins to remove a user from the 'user' table. Created by Jacob"""
        print('You can remove a student or instructor. Type "student" or "instructor"')
        userType = input('Would you like to remove an instructor or student? ')
        if(userType == 'student'):
          self.removeStudent(cursor)
        elif(userType == 'instructor'):
          self.removeInstructor(cursor)
        else:
          print('Invalid input')
          return
    def addUserToCourse(self, cursor):
      print('You can add a student or an instructor to a class. Type "student" or "instructor"')
      userType = input('Would you like to add an instructor or a student? ')
      if(userType == 'student'):
        self.addStudentToCourse(cursor)
      elif(userType == 'instructor'):
        self.addInstructorToCourse(cursor)
      else:
        print('Invalid input')
        return
    
    def addStudentToCourse(self, cursor):
        """Allows admins to add a student to a course. Created by Jacob."""
        while(1):
            if input("Add a student to a course. Hit enter to continue, or type 'exit' to go back: ") == 'exit' : return
            id = input('Student ID: ')
            crn = input("Course CRN: ")

            cursor.execute("SELECT * FROM COURSE WHERE CRN = '%s';" % (crn))
            course = cursor.fetchone()
            if course == None:
                print("Course not found") 
            else:
                try:
                  cursor.execute("""INSERT INTO SEMESTERSCHEDULE VALUES('%s', '%s', '%s');""" % (crn, course[8], id))
                  database.commit()
                except:
                    print('Course already in semester schedule')
    def addInstructorToCourse(self, cursor):
        """Allows admins to add an instructor to a course. Created by Jacob."""
        while(1):
            if input("Add an instructor to a course. Hit enter to continue, or type 'exit' to go back: ") == 'exit' : return
            instructorId = input('Instructor ID: ')
            crn = input("Course CRN: ")
            try:
              cursor.execute("""INSERT INTO SEMESTERSCHEDULE VALUES('%s', '%s', null);""" % (crn, instructorId))
            


              cursor.execute("SELECT * FROM COURSE WHERE CRN = '%s';" % (crn))
              course = cursor.fetchone()
              if course == None:
                  print("Course not found") 
              else:
                  try:
                      cursor.execute("""DELETE FROM COURSE WHERE CRN = '%s';""" % (crn))
                      cursor.execute("""INSERT INTO course VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');""" % (crn, course[1], course[2], course[3], course[4], course[5], course[6], course[7], instructorId)) 
                      database.commit()
                  except:
                      print('Error in removing instructor from course')



              database.commit()
            except:
                print('Course already in semester schedule')
    def removeUserFromCourse(self, cursor):
      print('You can remove a student or an instructor from a class. Type "student" or "instructor"')
      userType = input('Would you like to remove an instructor or a student? ')
      if(userType == 'student'):
        self.removeStudentFromCourse(cursor)
      elif(userType == 'instructor'):
        self.removeInstructorFromCourse(cursor)
      else:
        print('Invalid input')
        return
    def removeStudentFromCourse(self, cursor):
        """Allows admins to remove a user from a course. Created by Jacob."""
        while(1):
            if input("Remove student from courses. Hit enter to continue, or type 'exit' to go back: ") == 'exit' : return
            studentId = input('Student ID: ')
            crn = input("Course CRN: ")

            cursor.execute("SELECT * FROM COURSE WHERE CRN = '%s';" % (crn))
            course = cursor.fetchone()
            if course == None:
                print("Course not found") 
            else:
                try:
                    cursor.execute("""DELETE FROM SEMESTERSCHEDULE WHERE CRN = '%s' AND STUDENTID = '%s' AND INSTRUCTORID = '%s';""" % (crn, studentId, course[8]))
                    database.commit()
                except:
                    print('Course not in semester schedule')

    def removeInstructorFromCourse(self, cursor):
        """Allows admins to remove a user from a course. Created by Jacob."""
        while(1):
            if input("Remove instructor from courses. Hit enter to continue, or type 'exit' to go back: ") == 'exit' : return
            crn = input("Course CRN: ")
            cursor.execute("SELECT * FROM COURSE WHERE CRN = '%s';" % (crn))
            course = cursor.fetchone()
            if course == None:
                print("Course not found") 
            else:
                try:
                    cursor.execute("""DELETE FROM COURSE WHERE CRN = '%s';""" % (crn))
                    cursor.execute("""INSERT INTO course VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', null);""" % (crn, course[1], course[2], course[3], course[4], course[5], course[6], course[7])) 
                    database.commit()
                except:
                    print('Error in removing instructor from course')


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
        case 'TIME':
            time = input("Enter the start time of the course in the format 10:00:00 : ")
            cursor.execute("SELECT * FROM COURSE WHERE TIME='%s';" %time)
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
                user.createUser(cursor) 
            case 6:
                user.removeUser(cursor) 
            case 7:
                user.addUserToCourse(cursor) 
            case 8:
                user.removeUserFromCourse(cursor) 
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
        (4) Search course rosters
        (5) Save and log out\n""") 
        selection = int(choice)
        match selection:
            case 1:
                searchAll(cursor)
            case 2:
                searchParam(cursor)
            case 3:
                user.instructorPrintSchedule(cursor) 
            case 4:
                user.searchRosters(cursor)
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