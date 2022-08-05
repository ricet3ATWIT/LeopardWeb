#Script to seed courses to the database
import sqlite3

database = sqlite3.connect("src/main.db") 
# cursor objects are used to traverse, search, grab, etc. information from the database, similar to indices or pointers  
cursor = database.cursor() 

# delete values out of admin table
cursor.execute("DELETE FROM admin")


# drop the COURSE table if it exists
cursor.execute("DROP TABLE IF EXISTS COURSE")

# Drop semesterscheudle table if it exists
cursor.execute("DROP TABLE IF EXISTS SEMESTERSCHEDULE")


sql_command = """
CREATE TABLE COURSE (  
CRN CHAR(5) PRIMARY KEY NOT NULL,
TITLE TEXT NOT NULL,
DEPARTMENT CHAR(4) NOT NULL,
TIME DATETIME NOT NULL,
DAYSOFWEEK TEXT NOT NULL,
SEMESTER TEXT NOT NULL,
YEAR INTEGER NOT NULL,
CREDITS INTEGER NOT NULL,
INSTRUCTORID CHAR(5));
"""

cursor.execute(sql_command) 


# student is nullable so we can create a class with just an instructor
sql_command = """
CREATE TABLE SEMESTERSCHEDULE (  
CRN CHAR(5) NOT NULL,
INSTRUCTORID CHAR(5) NOT NULL,
STUDENTID CHAR(5), 
PRIMARY KEY (CRN, STUDENTID, INSTRUCTORID)
);
"""
cursor.execute(sql_command) 
# add 10 new courses
sql_command = """INSERT INTO COURSE VALUES(22000, 'Network Theory 1', 'BSEE', '10:00:00', 'TR', 'SUMMER', 2022, 4, 20001);"""
cursor.execute(sql_command) 

sql_command = """INSERT INTO COURSE VALUES(22004, 'Network Theory 2', 'BSEE', '12:00:00', 'TR', 'SUMMER', 2022, 4, 20001);"""
cursor.execute(sql_command) 

sql_command = """INSERT INTO COURSE VALUES(22001, 'Space 1', 'BSAS', '10:00:00', 'MWF', 'SUMMER', 2022, 4, 20002);"""
cursor.execute(sql_command) 

sql_command = """INSERT INTO COURSE VALUES(22005, 'Space 2', 'BSAS', '12:00:00', 'MWF', 'SUMMER', 2022, 4, 20002);"""
cursor.execute(sql_command) 

sql_command = """INSERT INTO COURSE VALUES(22002, 'Mechanics 1', 'BSME', '10:00:00', 'MWF', 'SUMMER', 2022, 4, 20003);"""
cursor.execute(sql_command) 

sql_command = """INSERT INTO COURSE VALUES(22006, 'Mechanics 2', 'BSME', '12:00:00', 'MWF', 'SUMMER', 2022, 4, 20003);"""
cursor.execute(sql_command) 

sql_command = """INSERT INTO COURSE VALUES(22007, 'Psycology 1', 'HUSS', '10:00:00', 'MWF', 'SUMMER', 2022, 4, 20004);"""
cursor.execute(sql_command) 

sql_command = """INSERT INTO COURSE VALUES(22008, 'Psycology 2', 'HUSS', '12:00:00', 'MWF', 'SUMMER', 2022, 4, 20004);"""
cursor.execute(sql_command) 

sql_command = """INSERT INTO COURSE VALUES(22009, 'Analog Circuit Design', 'BSEE', '08:00:00', 'MWF', 'SUMMER', 2022, 4, 20006);"""
cursor.execute(sql_command) 

sql_command = """INSERT INTO COURSE VALUES(22010, 'Microcontrollers with Assembly', 'BSEE', '10:00:00', 'MWF', 'SUMMER', 2022, 4, 20006);"""
cursor.execute(sql_command) 

# add 5 new students
sql_command = """INSERT INTO STUDENT VALUES(110011, 'Meerkat', 'Wild', '2022', 'BSEE', 'wildm', 'password');"""
cursor.execute(sql_command) 
sql_command = """INSERT INTO STUDENT VALUES(110012, 'Sour', 'Skittles', '2023', 'BSCO', 'skittles', 'password');"""
cursor.execute(sql_command) 
sql_command = """INSERT INTO STUDENT VALUES(110013, 'Yerba', 'Mate', '2024', 'BSEE', 'matey', 'password');"""
cursor.execute(sql_command) 
sql_command = """INSERT INTO STUDENT VALUES(110014, 'Robert', 'Pirsig', '2023', 'BSCO', 'pirsigr', 'password');"""
cursor.execute(sql_command) 
sql_command = """INSERT INTO STUDENT VALUES(110015, 'Paper', 'Towel', '2024', 'BSEE', 'towelp', 'password');"""
cursor.execute(sql_command) 

# add 1 admin
sql_command = """INSERT INTO ADMIN VALUES(30001, 'Margaret', 'Hamilton', 'President', 'Dobbs 1600', 'hamiltonm', 'password');"""
cursor.execute(sql_command) 


# add 10 instructors 
sql_command = """INSERT INTO INSTRUCTOR VALUES(20007, 'Harvey', 'Bryan', 'Associate Prof.', '2020', 'BSEE', 'bryanh', 'password');"""
cursor.execute(sql_command) 
sql_command = """INSERT INTO INSTRUCTOR VALUES(20008, 'Angie', 'Frazier', 'Associate Prof.', '2020', 'BSEE', 'fraziera', 'password');"""
cursor.execute(sql_command) 
sql_command = """INSERT INTO INSTRUCTOR VALUES(20009, 'Brandi', 'Bryant', 'Associate Prof.', '2020', 'BSEE', 'bryantb', 'password');"""
cursor.execute(sql_command) 
sql_command = """INSERT INTO INSTRUCTOR VALUES(20010, 'Hope', 'Murray', 'Associate Prof.', '2022', 'BSCO', 'murrayh', 'password');"""
cursor.execute(sql_command) 
sql_command = """INSERT INTO INSTRUCTOR VALUES(20011, 'Marta', 'Wagner', 'Associate Prof.', '2022', 'BSCO', 'wagnerm', 'password');"""
cursor.execute(sql_command) 
sql_command = """INSERT INTO INSTRUCTOR VALUES(20012, 'William', 'Hogan', 'Associate Prof.', '2022', 'BSCO', 'hoganw', 'password');"""
cursor.execute(sql_command) 
sql_command = """INSERT INTO INSTRUCTOR VALUES(20013, 'Hulk', 'Hogan', 'Associate Prof.', '2022', 'BSEE', 'hoganh', 'password');"""
cursor.execute(sql_command) 
sql_command = """INSERT INTO INSTRUCTOR VALUES(20014, 'Everett', 'Jenkins', 'Associate Prof.', '2022', 'BSCO', 'jenkinse', 'password');"""
cursor.execute(sql_command) 
sql_command = """INSERT INTO INSTRUCTOR VALUES(20015, 'Nina', 'West', 'Associate Prof.', '2022', 'BSCO', 'westn', 'password');"""
cursor.execute(sql_command) 
sql_command = """INSERT INTO INSTRUCTOR VALUES(20016, 'Ramiro', 'Reynolds', 'Associate Prof.', '2022', 'BSCO', 'reynoldsr', 'password');"""
cursor.execute(sql_command) 




sql_command = """INSERT INTO SEMESTERSCHEDULE VALUES(001, 00001, 20001);"""
cursor.execute(sql_command) 

print('successfully seeded courses')
database.commit()
database.close()
