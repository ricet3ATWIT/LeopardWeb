# Tests

## Add/Remove from Course Schedule - Jacob
Test Case 1
* Login as student
* add course to schedule
* remove same course from schedule
* logout

Run the following command:
```python
python3 src/tom/A5.py < testing/addRemoveFromStudentCourseSchedule1.txt 
```

expected output: 
``` 
Email: Password: Login successful!
STUDENT MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Add courses
        (4) Drop courses
        (5) Print schedule
        (6) Log out
Add courses to semester schedule. Hit enter to continue, or type 'exit' to go back: CRN: STUDENT MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Add courses
        (4) Drop courses
        (5) Print schedule
        (6) Log out
Add courses to semester schedule. Hit enter to continue, or type 'exit' to go back: CRN: STUDENT MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Add courses
        (4) Drop courses
        (5) Print schedule
        (6) Log out
```
**The test did match the expectations.**

Test Case 2
* Login as student
* add course to schedule
* add same course to schedule
   * should fail (print course already in schedule) 
* logout

run the following command:
```python
python3 src/tom/A5.py < testing/addRemoveFromStudentCourseSchedule2.txt 
```

expected output: 
```
Email: Password: Login successful!
STUDENT MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Add courses
        (4) Drop courses
        (5) Print schedule
        (6) Log out
Add courses to semester schedule. Hit enter to continue, or type 'exit' to go back: CRN: STUDENT MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Add courses
        (4) Drop courses
        (5) Print schedule
        (6) Log out
Add courses to semester schedule. Hit enter to continue, or type 'exit' to go back: CRN: Course already in semester schedule
STUDENT MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Add courses
        (4) Drop courses
        (5) Print schedule
        (6) Log out
Add courses to semester schedule. Hit enter to continue, or type 'exit' to go back: CRN: STUDENT MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Add courses
        (4) Drop courses
        (5) Print schedule
        (6) Log out
```
**The test did match the expectations.**

## Assemble and Print Instructor Course Roster - Jacob
Test Case 1
* Login as instructor
* print course roster
* Logout

run the following command:
```python
python3 src/tom/A5.py < testing/printInstructorCourseRoster1.txt 
```

expected output: 
```
Email: Password: Login successful!
INSTRUCTOR MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Print teaching schedule
        (4) Search other teaching schedules 
        (5) Log out
-----------------------------------------------------
Course Name: Network Theory 1
CRN: 1
Department: BSEE
Time: 10:00:00
Days of the Week: TR
Semester: SUMMER
Year: 2022
Credits: 4
INSTRUCTOR MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Print teaching schedule
        (4) Search other teaching schedules 
        (5) Log out
```
**The test did match the expectations.**

# Add/remove courses from the system as an Admin - Jacob
Test Case 1
* Login as admin
* add course with the same CRN as a course in the system
  * should fail (Error in parameter inputs)
* add correct course to system
* search for course with CRN
  * should find and print course
* add same course to system
   * should fail (print course already in system)
* remove course from system
* remove same course from system
   * should print an empty list for Course selected
* logout

run the following command:
```python
python3 src/tom/A5.py < testing/addRemoveFromAdminCourseSystem1.txt 
```

expected output: 
```
Email: Password: Login successful!
ADMIN MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Add courses to system
        (4) Remove courses from system
        (5) Add user to system
        (6) Remove user from system
        (7) Link user to course
        (8) Remove links
        (9) Log out
Add courses. Hit enter to continue, or type 'exit' to go back: CRN: Course title: Department (four letter abbr.): Meeting time: Meeting days: Semester: Year: Credits: Error in parameter inputs.
Add courses. Hit enter to continue, or type 'exit' to go back: CRN: Course title: Department (four letter abbr.): Meeting time: Meeting days: Semester: Year: Credits: Add courses. Hit enter to continue, or type 'exit' to go back: ADMIN MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Add courses to system
        (4) Remove courses from system
        (5) Add user to system
        (6) Remove user from system
        (7) Link user to course
        (8) Remove links
        (9) Log out
Params: CRN, TITLE, DEPARTMENT, TIME, DAY, SEMESTER, YEAR, CREDITS, INSTRUCTORID
Enter a parameter: Enter a CRN: -----------------------------------------------------
Course Name: Testing
CRN: 99
Department: ELEC
Time: 10 am
Days of the Week: TR
Semester: Summer
Year: 2022
Credits: 4
ADMIN MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Add courses to system
        (4) Remove courses from system
        (5) Add user to system
        (6) Remove user from system
        (7) Link user to course
        (8) Remove links
        (9) Log out
Remove courses. Hit enter to continue, or type 'exit' to go back: Input the CRN of the course to delete: Course selected: [('99', 'Testing', 'ELEC', '10 am', 'TR', 'Summer', 2022, 4, '0')]
Confirm deletion? (y/n): Remove courses. Hit enter to continue, or type 'exit' to go back: Input the CRN of the course to delete: Course selected: []
Confirm deletion? (y/n): Remove courses. Hit enter to continue, or type 'exit' to go back: ADMIN MENU:
        (1) Search courses
        (2) Search courses (with parameters)
        (3) Add courses to system
        (4) Remove courses from system
        (5) Add user to system
        (6) Remove user from system
        (7) Link user to course
        (8) Remove links
        (9) Log out
```
**The test did match the expectations.**