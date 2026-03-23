# Hussein Alsawafi & Mira
# CIS 298 - Week 9 Assignment
# Registration Database - managing all tables + student transcript

import sqlite3

connection = sqlite3.connect('registration.sqlite')
cursor = connection.cursor()

# create all the tables if they don't exist yet
# we need Faculty, Student, Course, Section, and Enrollment
cursor.executescript('''
    CREATE TABLE IF NOT EXISTS Faculty (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        name  TEXT NOT NULL,
        email TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS Student (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        name  TEXT NOT NULL,
        email TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS Course (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        Department TEXT NOT NULL,
        Number     TEXT NOT NULL,
        Credits    INTEGER NOT NULL
    );
    CREATE TABLE IF NOT EXISTS Section (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        Course_ID  INTEGER NOT NULL,
        Faculty_ID INTEGER NOT NULL,
        Semester   TEXT NOT NULL,
        FOREIGN KEY (Course_ID)  REFERENCES Course(id),
        FOREIGN KEY (Faculty_ID) REFERENCES Faculty(id)
    );
    CREATE TABLE IF NOT EXISTS Enrollment (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        Student_ID INTEGER NOT NULL,
        Section_ID INTEGER NOT NULL,
        Grade      TEXT,
        FOREIGN KEY (Student_ID) REFERENCES Student(id),
        FOREIGN KEY (Section_ID) REFERENCES Section(id)
    );
''')
connection.commit()


def print_menu():
    print("\n--- Registration System ---")
    print("1 - Manage Faculty")
    print("2 - Manage Students")
    print("3 - Manage Courses")
    print("4 - Manage Sections")
    print("5 - Manage Enrollments")
    print("6 - View Student Transcript")
    print("QUIT - Exit")


# --- Faculty ---
def manage_faculty():
    action = input("Enter 1 for List Faculty, 2 for Add Faculty, 3 for Update Faculty, 4 for Delete Faculty: ")

    if action == "1":
        cursor.execute('SELECT * FROM Faculty')
        print("id, name, email")
        for row in cursor:
            print(row)

    elif action == "2":
        name = input("Enter name: ")
        email = input("Enter email: ")
        cursor.execute('INSERT INTO Faculty (name, email) VALUES (?, ?)', (name, email))
        connection.commit()
        print("Faculty added!")

    elif action == "3":
        id = int(input("Enter the ID to update: "))
        name = input("Enter name: ")
        email = input("Enter email: ")
        cursor.execute('UPDATE Faculty SET name = ?, email = ? WHERE id = ?', (name, email, id))
        connection.commit()
        print("Faculty updated!")

    elif action == "4":
        id = int(input("Enter the ID to delete: "))
        cursor.execute('DELETE FROM Faculty WHERE id = ?', (id,))
        connection.commit()
        print("Faculty deleted!")


# --- Students (Hussein did this part) ---
def manage_students():
    action = input("Enter 1 for List Students, 2 for Add Student, 3 for Update Student, 4 for Delete Student: ")

    if action == "1":
        cursor.execute('SELECT * FROM Student')
        print("id, name, email")
        for row in cursor:
            print(row)

    elif action == "2":
        name = input("Enter name: ")
        email = input("Enter email: ")
        cursor.execute('INSERT INTO Student (name, email) VALUES (?, ?)', (name, email))
        connection.commit()
        print("Student added!")

    elif action == "3":
        id = int(input("Enter the ID to update: "))
        name = input("Enter name: ")
        email = input("Enter email: ")
        cursor.execute('UPDATE Student SET name = ?, email = ? WHERE id = ?', (name, email, id))
        connection.commit()
        print("Student updated!")

    elif action == "4":
        id = int(input("Enter the ID to delete: "))
        cursor.execute('DELETE FROM Student WHERE id = ?', (id,))
        connection.commit()
        print("Student deleted!")


# --- Courses ---
def manage_courses():
    action = input("Enter 1 for List Courses, 2 for Add Course, 3 for Update Course, 4 for Delete Course: ")

    if action == "1":
        cursor.execute('SELECT * FROM Course')
        print("id, Department, Number, Credits")
        for row in cursor:
            print(row)

    elif action == "2":
        department = input("Enter department (ex: CIS): ")
        number = input("Enter course number (ex: 298): ")
        credits = int(input("Enter number of credits: "))
        cursor.execute('INSERT INTO Course (Department, Number, Credits) VALUES (?, ?, ?)',
                       (department, number, credits))
        connection.commit()
        print("Course added!")

    elif action == "3":
        id = int(input("Enter the ID to update: "))
        department = input("Enter department: ")
        number = input("Enter course number: ")
        credits = int(input("Enter credits: "))
        cursor.execute('UPDATE Course SET Department = ?, Number = ?, Credits = ? WHERE id = ?',
                       (department, number, credits, id))
        connection.commit()
        print("Course updated!")

    elif action == "4":
        id = int(input("Enter the ID to delete: "))
        cursor.execute('DELETE FROM Course WHERE id = ?', (id,))
        connection.commit()
        print("Course deleted!")


# --- Sections (Mira did this part) ---
def manage_sections():
    action = input("Enter 1 for List Sections, 2 for Add Section, 3 for Update Section, 4 for Delete Section: ")

    if action == "1":
        # joined so we can see the actual course name and instructor instead of just ids
        cursor.execute('''
            SELECT Section.id, Course.Department, Course.Number, Faculty.name, Section.Semester
            FROM Section
            INNER JOIN Course ON Course.id = Section.Course_ID
            INNER JOIN Faculty ON Faculty.id = Section.Faculty_ID
        ''')
        print("id, Department, Course Number, Instructor, Semester")
        for row in cursor:
            print(row)

    elif action == "2":
        # show available courses and faculty first so user knows what IDs to pick
        print("Available Courses:")
        cursor.execute('SELECT id, Department, Number FROM Course')
        for row in cursor:
            print(row)
        course_id = int(input("Enter Course ID: "))

        print("Available Faculty:")
        cursor.execute('SELECT id, name FROM Faculty')
        for row in cursor:
            print(row)
        faculty_id = int(input("Enter Faculty ID: "))

        semester = input("Enter semester (ex: Winter 2026): ")
        cursor.execute('INSERT INTO Section (Course_ID, Faculty_ID, Semester) VALUES (?, ?, ?)',
                       (course_id, faculty_id, semester))
        connection.commit()
        print("Section added!")

    elif action == "3":
        id = int(input("Enter the Section ID to update: "))
        course_id = int(input("Enter new Course ID: "))
        faculty_id = int(input("Enter new Faculty ID: "))
        semester = input("Enter new semester: ")
        cursor.execute('UPDATE Section SET Course_ID = ?, Faculty_ID = ?, Semester = ? WHERE id = ?',
                       (course_id, faculty_id, semester, id))
        connection.commit()
        print("Section updated!")

    elif action == "4":
        id = int(input("Enter the Section ID to delete: "))
        cursor.execute('DELETE FROM Section WHERE id = ?', (id,))
        connection.commit()
        print("Section deleted!")


# --- Enrollments ---
def manage_enrollments():
    action = input("Enter 1 for List Enrollments, 2 for Add Enrollment, 3 for Update Grade, 4 for Delete Enrollment: ")

    if action == "1":
        # join everything so it's readable
        cursor.execute('''
            SELECT Enrollment.id, Student.name, Course.Department, Course.Number, Section.Semester, Enrollment.Grade
            FROM Enrollment
            INNER JOIN Student ON Student.id = Enrollment.Student_ID
            INNER JOIN Section ON Section.id = Enrollment.Section_ID
            INNER JOIN Course ON Course.id = Section.Course_ID
        ''')
        print("id, Student, Department, Course Number, Semester, Grade")
        for row in cursor:
            print(row)

    elif action == "2":
        print("Available Students:")
        cursor.execute('SELECT id, name FROM Student')
        for row in cursor:
            print(row)
        student_id = int(input("Enter Student ID: "))

        print("Available Sections:")
        cursor.execute('''
            SELECT Section.id, Course.Department, Course.Number, Section.Semester
            FROM Section
            INNER JOIN Course ON Course.id = Section.Course_ID
        ''')
        for row in cursor:
            print(row)
        section_id = int(input("Enter Section ID: "))

        grade = input("Enter grade (leave blank if not graded yet): ").strip()
        if grade == "":
            grade = None
        cursor.execute('INSERT INTO Enrollment (Student_ID, Section_ID, Grade) VALUES (?, ?, ?)',
                       (student_id, section_id, grade))
        connection.commit()
        print("Enrollment added!")

    elif action == "3":
        id = int(input("Enter Enrollment ID to update grade: "))
        grade = input("Enter new grade: ")
        cursor.execute('UPDATE Enrollment SET Grade = ? WHERE id = ?', (grade, id))
        connection.commit()
        print("Grade updated!")

    elif action == "4":
        id = int(input("Enter Enrollment ID to delete: "))
        cursor.execute('DELETE FROM Enrollment WHERE id = ?', (id,))
        connection.commit()
        print("Enrollment deleted!")


# --- Transcript ---
# this uses the join query from the assignment comments
def show_transcript():
    print("Available Students:")
    cursor.execute('SELECT id, name FROM Student')
    for row in cursor:
        print(row)

    student_id = int(input("Enter Student ID to view transcript: "))

    # get the student name first
    cursor.execute('SELECT name FROM Student WHERE id = ?', (student_id,))
    result = cursor.fetchone()
    if not result:
        print("Student not found.")
        return

    student_name = result[0]

    # the join query from the assignment - grabs department, course number, credits, and grade
    cursor.execute('''
        SELECT Course.Department, Course.Number, Course.Credits, Enrollment.Grade
        FROM Enrollment
        INNER JOIN Student ON Student.id = Enrollment.Student_ID
        INNER JOIN Section ON Section.id = Enrollment.Section_ID
        INNER JOIN Course ON Course.id = Section.Course_ID
        WHERE Student_ID = ?
    ''', (student_id,))

    rows = cursor.fetchall()

    print("\n========================================")
    print(f"Transcript for: {student_name}")
    print("========================================")
    print(f"{'Dept':<10} {'Number':<10} {'Credits':<10} {'Grade'}")
    print("-" * 40)

    total_credits = 0
    total_points = 0
    grade_map = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}

    for row in rows:
        dept, number, credits, grade = row
        if grade is None:
            grade = "In Progress"
        print(f"{dept:<10} {number:<10} {credits:<10} {grade}")

        # only count completed grades toward GPA
        if grade in grade_map:
            total_credits += credits
            total_points += grade_map[grade] * credits

    print("-" * 40)
    if total_credits > 0:
        gpa = total_points / total_credits
        print(f"Credits Completed: {total_credits}")
        print(f"GPA: {gpa:.2f}")
    else:
        print("No completed courses yet.")
    print("========================================\n")


# --- main loop ---
choice = ""
while choice != "QUIT":
    print_menu()
    choice = input("Enter a choice: ").strip().upper()

    if choice == "1":
        manage_faculty()
    elif choice == "2":
        manage_students()
    elif choice == "3":
        manage_courses()
    elif choice == "4":
        manage_sections()
    elif choice == "5":
        manage_enrollments()
    elif choice == "6":
        show_transcript()
    elif choice != "QUIT":
        print("Invalid choice, try again.")

connection.close()
print("Bye!")
