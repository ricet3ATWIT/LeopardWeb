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
    # login/logout, search, search(parameters)

class Student(User):
    def testS(self):
        print("TestS")
    #add/drop courses

class Instructor(User):
    def testI(self):
        print("TestI")
    #assemble and print course roster

class Admin(User):
    def testA(self):
        print("TestA")
    #create/remove courses

    def createCourse(cursor):
        """Allows admins to add a course to the 'course' table. Created by Tom."""
        while(1):
            if input("Add courses. Hit enter to continue, or type 'exit' to go back: ") == 'exit' : break
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
            crn = input("Input the CRN of the course to delete (or type 'exit' to go back): ")
            if crn == 'exit' : return
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
    """Prints all courses. Created by Tom."""
    cursor.execute("SELECT * FROM courses;")
    print(cursor.fetchall())     
            


## Driver Code
# database file connection 
database = sqlite3.connect("src/assignment5.db") 

# cursor objects are used to traverse, search, grab, etc. information from the database, similar to indices or pointers  
cursor = database.cursor() 

login(cursor)


# To save the changes in the files. Never skip this.  
# If we skip this, nothing will be saved in the database. 
database.commit() 
  
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
    if query_result == []:
        print("No instructors available.")
    for i in query_result:
	    print(i)

#while(1):
#    choice = input("""MENU:
#    (1) Search database
#    (2) Print entire database
#    (3) Create (course) table
#    (4) Insert (student) tuples
#    (5) Update (admin) tuples
#    (6) Remove tuples
#    (7) Insert (course) tuples
#    (8) Potential Intructor Query
#    (9) Exit the program\n""")
#    selection = int(choice)
#    match selection:
#        case 1:
#            searchDB(cursor)
#        case 2:
#            printDB(cursor)
#        case 3:
#            createTable(cursor)
#        case 4:
#            insert(cursor)
#        case 5:
#            update(cursor)
#        case 6:
#            remove(cursor)
#        case 7:
#            insert2(cursor)
#        case 8:
#            potInt(cursor)
#        case 9:
#            break
#        case default:
#            print("Not a valid selection. Use characters '1', '2', etc.")


