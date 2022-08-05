#Script to seed courses to the database
import sqlite3

database = sqlite3.connect("src/main.db") 
# cursor objects are used to traverse, search, grab, etc. information from the database, similar to indices or pointers  
cursor = database.cursor() 

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
INSTRUCTORID CHAR(5) NOT NULL);
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

sql_command = """INSERT INTO COURSE VALUES(00001, 'Network Theory 1', 'BSEE', '10:00:00', 'TR', 'SUMMER', 2022, 4, 20001);"""
cursor.execute(sql_command) 

sql_command = """INSERT INTO COURSE VALUES(00002, 'Space 1', 'BSAS', '10:00:00', 'MWF', 'SUMMER', 2022, 4, 20002);"""
cursor.execute(sql_command) 

sql_command = """INSERT INTO COURSE VALUES(00003, 'Mechanics 1', 'BSME', '10:00:00', 'MWF', 'SUMMER', 2022, 4, 20003);"""
cursor.execute(sql_command) 

sql_command = """INSERT INTO COURSE VALUES(00004, 'Psycology 1', 'HUSS', '10:00:00', 'MWF', 'SUMMER', 2022, 4, 20004);"""
cursor.execute(sql_command) 

sql_command = """INSERT INTO SEMESTERSCHEDULE VALUES(001, 00001, 20001);"""
cursor.execute(sql_command) 

print('successfully seeded courses')
database.commit()
database.close()
