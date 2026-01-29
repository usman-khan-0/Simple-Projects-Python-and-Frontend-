"""
Menu module for University Management System
"""

from typing import Optional
from university import University
from student import Student
from faculty import Faculty
from course import Course
from department import Department
import sys

class Menu:
    """Handles the menu interface for the University Management System."""
    
    @staticmethod
    def display_main_menu(university: University) -> None:
        """Display the main menu and handle user input."""
        while True:
            print("\n" + "="*50)
            print("MAIN MENU")
            print("="*50)
            print("1. Student Management")
            print("2. Faculty Management")
            print("3. Course Management")
            print("4. Department Management")
            print("5. University Operations")
            print("6. Display Statistics")
            print("7. Search Operations")
            print("8. Generate Sample Data")
            print("0. Exit")
            print("="*50)
            
            choice = input("\nEnter your choice (0-8): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                Menu.display_student_menu(university)
            elif choice == '2':
                Menu.display_faculty_menu(university)
            elif choice == '3':
                Menu.display_course_menu(university)
            elif choice == '4':
                Menu.display_department_menu(university)
            elif choice == '5':
                Menu.display_operations_menu(university)
            elif choice == '6':
                university.display_detailed_stats()
            elif choice == '7':
                Menu.display_search_menu(university)
            elif choice == '8':
                Menu.generate_sample_data(university)
            else:
                print("⚠ Invalid choice! Please try again.")
            
            input("\nPress Enter to continue...")
    
    @staticmethod
    def display_student_menu(university: University) -> None:
        """Display student management menu."""
        while True:
            print("\n" + "="*50)
            print("STUDENT MANAGEMENT")
            print("="*50)
            print("1. Add New Student")
            print("2. View All Students")
            print("3. Search Student by ID")
            print("4. Update Student Information")
            print("5. Delete Student")
            print("6. View Student Courses & Grades")
            print("7. Assign Grade to Student")
            print("8. Sort Students by GPA")
            print("0. Back to Main Menu")
            print("="*50)
            
            choice = input("\nEnter your choice (0-8): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                Menu.add_student(university)
            elif choice == '2':
                Menu.view_all_students(university)
            elif choice == '3':
                Menu.search_student_by_id(university)
            elif choice == '4':
                Menu.update_student(university)
            elif choice == '5':
                Menu.delete_student(university)
            elif choice == '6':
                Menu.view_student_courses(university)
            elif choice == '7':
                Menu.assign_grade(university)
            elif choice == '8':
                Menu.sort_students_by_gpa(university)
            else:
                print("⚠ Invalid choice! Please try again.")
            
            if choice != '0':
                input("\nPress Enter to continue...")
    
    @staticmethod
    def add_student(university: University) -> None:
        """Add a new student."""
        print("\n" + "="*50)
        print("ADD NEW STUDENT")
        print("="*50)
        
        try:
            student_id = input("Enter Student ID (format: S0001): ").strip()
            if not Student.is_valid_student_id(student_id):
                print("⚠ Invalid student ID format! Use format: S0001")
                return
            
            if university.find_student(student_id):
                print("⚠ Student ID already exists!")
                return
            
            name = input("Enter Full Name: ").strip()
            if not name:
                print("⚠ Name cannot be empty!")
                return
            
            age = input("Enter Age: ").strip()
            if not age.isdigit() or int(age) <= 0:
                print("⚠ Invalid age! Age must be a positive number.")
                return
            age = int(age)
            
            gender = input("Enter Gender (M/F/Other): ").strip()
            if not gender:
                gender = "Other"
            
            # Show available departments
            if university.departments:
                print("\nAvailable Departments:")
                for dept in university.departments:
                    print(f"  {dept.department_id}: {dept.name}")
            
            department = input("Enter Department ID: ").strip().upper()
            
            # Create new student
            student = Student(student_id, name, age, gender, department)
            
            if university.add_student(student):
                print(f"✓ Student {name} added successfully!")
            else:
                print("⚠ Failed to add student!")
        
        except ValueError as e:
            print(f"⚠ Error: {e}")
        except Exception as e:
            print(f"⚠ An unexpected error occurred: {e}")
    
    @staticmethod
    def view_all_students(university: University) -> None:
        """View all students."""
        if not university.students:
            print("\nNo students found in the system.")
            return
        
        print("\n" + "="*80)
        print("ALL STUDENTS")
        print("="*80)
        print(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Gender':<8} {'Department':<15} {'GPA':<6}")
        print("-"*80)
        
        for student in university.students:
            print(f"{student.student_id:<10} {student.name:<20} {student.age:<5} "
                  f"{student.gender:<8} {student.department:<15} {student.gpa:<6.2f}")
        
        print("="*80)
        print(f"Total Students: {len(university.students)}")
    
    @staticmethod
    def search_student_by_id(university: University) -> None:
        """Search for a student by ID."""
        student_id = input("Enter Student ID to search: ").strip()
        
        student = university.find_student(student_id)
        if student:
            student.display_info()
        else:
            print(f"⚠ Student with ID {student_id} not found!")
    
    @staticmethod
    def update_student(university: University) -> None:
        """Update student information."""
        student_id = input("Enter Student ID to update: ").strip()
        
        student = university.find_student(student_id)
        if not student:
            print(f"⚠ Student with ID {student_id} not found!")
            return
        
        student.display_info()
        print("\n" + "="*50)
        print("UPDATE STUDENT INFORMATION")
        print("="*50)
        print("Leave field blank to keep current value.")
        
        try:
            name = input(f"New Name [{student.name}]: ").strip()
            if name:
                student.name = name
            
            age_str = input(f"New Age [{student.age}]: ").strip()
            if age_str:
                if not age_str.isdigit() or int(age_str) <= 0:
                    print("⚠ Invalid age! Age must be a positive number.")
                    return
                student.age = int(age_str)
            
            gender = input(f"New Gender [{student.gender}]: ").strip()
            if gender:
                student.gender = gender
            
            department = input(f"New Department [{student.department}]: ").strip()
            if department:
                student.department = department
            
            print(f"✓ Student {student_id} updated successfully!")
        
        except Exception as e:
            print(f"⚠ Error updating student: {e}")
    
    @staticmethod
    def delete_student(university: University) -> None:
        """Delete a student."""
        student_id = input("Enter Student ID to delete: ").strip()
        
        student = university.find_student(student_id)
        if not student:
            print(f"⚠ Student with ID {student_id} not found!")
            return
        
        # Confirm deletion
        print(f"\nStudent to delete:")
        student.display_info()
        confirm = input("\nAre you sure you want to delete this student? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            if university.remove_student(student_id):
                print(f"✓ Student {student_id} deleted successfully!")
            else:
                print("⚠ Failed to delete student!")
        else:
            print("Deletion cancelled.")
    
    @staticmethod
    def view_student_courses(university: University) -> None:
        """View student courses and grades."""
        student_id = input("Enter Student ID: ").strip()
        
        student = university.find_student(student_id)
        if student:
            student.display_info()
            student.display_course_grades()
        else:
            print(f"⚠ Student with ID {student_id} not found!")
    
    @staticmethod
    def assign_grade(university: University) -> None:
        """Assign a grade to a student for a course."""
        student_id = input("Enter Student ID: ").strip()
        course_id = input("Enter Course ID: ").strip()
        
        try:
            grade = float(input("Enter Grade (0.0-4.0): ").strip())
            if not 0.0 <= grade <= 4.0:
                print("⚠ Grade must be between 0.0 and 4.0!")
                return
            
            if university.assign_grade(student_id, course_id, grade):
                print(f"✓ Grade assigned successfully!")
            else:
                print("⚠ Failed to assign grade! Check if student is enrolled in the course.")
        
        except ValueError:
            print("⚠ Invalid grade! Please enter a number.")
    
    @staticmethod
    def sort_students_by_gpa(university: University) -> None:
        """Display students sorted by GPA."""
        if not university.students:
            print("\nNo students found in the system.")
            return
        
        order = input("Sort order (1=High to Low, 2=Low to High): ").strip()
        descending = True if order == '1' else False
        
        sorted_students = university.sort_students_by_gpa(descending)
        
        order_text = "HIGHEST TO LOWEST" if descending else "LOWEST TO HIGHEST"
        print(f"\n" + "="*80)
        print(f"STUDENTS SORTED BY GPA ({order_text})")
        print("="*80)
        print(f"{'ID':<10} {'Name':<20} {'Department':<15} {'GPA':<6} {'Courses':<10}")
        print("-"*80)
        
        for student in sorted_students:
            print(f"{student.student_id:<10} {student.name:<20} "
                  f"{student.department:<15} {student.gpa:<6.2f} "
                  f"{len(student.course_grades):<10}")
    
    @staticmethod
    def display_faculty_menu(university: University) -> None:
        """Display faculty management menu."""
        while True:
            print("\n" + "="*50)
            print("FACULTY MANAGEMENT")
            print("="*50)
            print("1. Add New Faculty")
            print("2. View All Faculty")
            print("3. Search Faculty by ID")
            print("4. Update Faculty Information")
            print("5. Delete Faculty")
            print("6. View Faculty Courses")
            print("0. Back to Main Menu")
            print("="*50)
            
            choice = input("\nEnter your choice (0-6): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                Menu.add_faculty(university)
            elif choice == '2':
                Menu.view_all_faculty(university)
            elif choice == '3':
                Menu.search_faculty_by_id(university)
            elif choice == '4':
                Menu.update_faculty(university)
            elif choice == '5':
                Menu.delete_faculty(university)
            elif choice == '6':
                Menu.view_faculty_courses(university)
            else:
                print("⚠ Invalid choice! Please try again.")
            
            if choice != '0':
                input("\nPress Enter to continue...")
    
    @staticmethod
    def add_faculty(university: University) -> None:
        """Add a new faculty member."""
        print("\n" + "="*50)
        print("ADD NEW FACULTY")
        print("="*50)
        
        try:
            faculty_id = input("Enter Faculty ID (format: F0001): ").strip()
            if not Faculty.is_valid_faculty_id(faculty_id):
                print("⚠ Invalid faculty ID format! Use format: F0001")
                return
            
            if university.find_faculty(faculty_id):
                print("⚠ Faculty ID already exists!")
                return
            
            name = input("Enter Full Name: ").strip()
            if not name:
                print("⚠ Name cannot be empty!")
                return
            
            # Show available departments
            if university.departments:
                print("\nAvailable Departments:")
                for dept in university.departments:
                    print(f"  {dept.department_id}: {dept.name}")
            
            department = input("Enter Department ID: ").strip().upper()
            
            # Create new faculty
            faculty = Faculty(faculty_id, name, department)
            
            if university.add_faculty(faculty):
                print(f"✓ Faculty {name} added successfully!")
            else:
                print("⚠ Failed to add faculty!")
        
        except ValueError as e:
            print(f"⚠ Error: {e}")
        except Exception as e:
            print(f"⚠ An unexpected error occurred: {e}")
    
    @staticmethod
    def view_all_faculty(university: University) -> None:
        """View all faculty members."""
        if not university.faculty:
            print("\nNo faculty members found in the system.")
            return
        
        print("\n" + "="*70)
        print("ALL FACULTY MEMBERS")
        print("="*70)
        print(f"{'ID':<10} {'Name':<20} {'Department':<15} {'Courses':<10}")
        print("-"*70)
        
        for faculty in university.faculty:
            print(f"{faculty.faculty_id:<10} {faculty.name:<20} "
                  f"{faculty.department:<15} {len(faculty.courses_taught):<10}")
        
        print("="*70)
        print(f"Total Faculty: {len(university.faculty)}")
    
    @staticmethod
    def search_faculty_by_id(university: University) -> None:
        """Search for a faculty member by ID."""
        faculty_id = input("Enter Faculty ID to search: ").strip()
        
        faculty = university.find_faculty(faculty_id)
        if faculty:
            faculty.display_info()
        else:
            print(f"⚠ Faculty with ID {faculty_id} not found!")
    
    # ... (Similar methods for update_faculty, delete_faculty, view_faculty_courses)
    
    @staticmethod
    def display_course_menu(university: University) -> None:
        """Display course management menu."""
        while True:
            print("\n" + "="*50)
            print("COURSE MANAGEMENT")
            print("="*50)
            print("1. Add New Course")
            print("2. View All Courses")
            print("3. Search Course by ID")
            print("4. Update Course Information")
            print("5. Delete Course")
            print("6. Assign Faculty to Course")
            print("7. Enroll Student in Course")
            print("0. Back to Main Menu")
            print("="*50)
            
            choice = input("\nEnter your choice (0-7): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                Menu.add_course(university)
            elif choice == '2':
                Menu.view_all_courses(university)
            elif choice == '3':
                Menu.search_course_by_id(university)
            elif choice == '4':
                Menu.update_course(university)
            elif choice == '5':
                Menu.delete_course(university)
            elif choice == '6':
                Menu.assign_faculty_to_course_menu(university)
            elif choice == '7':
                Menu.enroll_student_in_course_menu(university)
            else:
                print("⚠ Invalid choice! Please try again.")
            
            if choice != '0':
                input("\nPress Enter to continue...")
    
    @staticmethod
    def add_course(university: University) -> None:
        """Add a new course."""
        print("\n" + "="*50)
        print("ADD NEW COURSE")
        print("="*50)
        
        try:
            course_id = input("Enter Course ID (format: CSE101): ").strip().upper()
            if not Course.is_valid_course_id(course_id):
                print("⚠ Invalid course ID format! Use format like CSE101")
                return
            
            if university.find_course(course_id):
                print("⚠ Course ID already exists!")
                return
            
            name = input("Enter Course Name: ").strip()
            if not name:
                print("⚠ Course name cannot be empty!")
                return
            
            credit_hours = input("Enter Credit Hours: ").strip()
            if not credit_hours.isdigit() or int(credit_hours) <= 0:
                print("⚠ Credit hours must be a positive number!")
                return
            credit_hours = int(credit_hours)
            
            # Create new course
            course = Course(course_id, name, credit_hours)
            
            # Add to department
            dept_id = input("Enter Department ID for this course: ").strip().upper()
            department = university.find_department(dept_id)
            if department:
                department.add_course(course_id)
            
            if university.add_course(course):
                print(f"✓ Course {name} added successfully!")
            else:
                print("⚠ Failed to add course!")
        
        except ValueError as e:
            print(f"⚠ Error: {e}")
        except Exception as e:
            print(f"⚠ An unexpected error occurred: {e}")
    
    @staticmethod
    def view_all_courses(university: University) -> None:
        """View all courses."""
        if not university.courses:
            print("\nNo courses found in the system.")
            return
        
        print("\n" + "="*90)
        print("ALL COURSES")
        print("="*90)
        print(f"{'ID':<10} {'Name':<25} {'Credits':<8} {'Faculty':<12} {'Students':<10}")
        print("-"*90)
        
        for course in university.courses:
            print(f"{course.course_id:<10} {course.name:<25} "
                  f"{course.credit_hours:<8} {course.assigned_faculty if course.assigned_faculty else 'None':<12} "
                  f"{len(course.enrolled_students):<10}")
        
        print("="*90)
        print(f"Total Courses: {len(university.courses)}")
    
    @staticmethod
    def assign_faculty_to_course_menu(university: University) -> None:
        """Assign faculty to a course."""
        course_id = input("Enter Course ID: ").strip()
        faculty_id = input("Enter Faculty ID: ").strip()
        
        if university.assign_faculty_to_course(faculty_id, course_id):
            print(f"✓ Faculty {faculty_id} assigned to course {course_id} successfully!")
        else:
            print("⚠ Failed to assign faculty to course! Check if both exist.")
    
    @staticmethod
    def enroll_student_in_course_menu(university: University) -> None:
        """Enroll a student in a course."""
        student_id = input("Enter Student ID: ").strip()
        course_id = input("Enter Course ID: ").strip()
        
        if university.enroll_student_in_course(student_id, course_id):
            print(f"✓ Student {student_id} enrolled in course {course_id} successfully!")
        else:
            print("⚠ Failed to enroll student in course! Check if both exist.")
    
    @staticmethod
    def display_department_menu(university: University) -> None:
        """Display department management menu."""
        while True:
            print("\n" + "="*50)
            print("DEPARTMENT MANAGEMENT")
            print("="*50)
            print("1. Add New Department")
            print("2. View All Departments")
            print("3. Search Department by ID")
            print("4. Update Department Information")
            print("5. Delete Department")
            print("6. Set Head of Department")
            print("0. Back to Main Menu")
            print("="*50)
            
            choice = input("\nEnter your choice (0-6): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                Menu.add_department(university)
            elif choice == '2':
                Menu.view_all_departments(university)
            elif choice == '3':
                Menu.search_department_by_id(university)
            elif choice == '4':
                Menu.update_department(university)
            elif choice == '5':
                Menu.delete_department(university)
            elif choice == '6':
                Menu.set_head_of_department(university)
            else:
                print("⚠ Invalid choice! Please try again.")
            
            if choice != '0':
                input("\nPress Enter to continue...")
    
    @staticmethod
    def add_department(university: University) -> None:
        """Add a new department."""
        print("\n" + "="*50)
        print("ADD NEW DEPARTMENT")
        print("="*50)
        
        try:
            department_id = input("Enter Department ID (2-4 uppercase letters, e.g., CSE): ").strip().upper()
            if not Department.is_valid_department_id(department_id):
                print("⚠ Invalid department ID! Use 2-4 uppercase letters.")
                return
            
            if university.find_department(department_id):
                print("⚠ Department ID already exists!")
                return
            
            name = input("Enter Department Name: ").strip()
            if not name:
                print("⚠ Department name cannot be empty!")
                return
            
            # Create new department
            department = Department(department_id, name)
            
            if university.add_department(department):
                print(f"✓ Department {name} added successfully!")
            else:
                print("⚠ Failed to add department!")
        
        except ValueError as e:
            print(f"⚠ Error: {e}")
        except Exception as e:
            print(f"⚠ An unexpected error occurred: {e}")
    
    @staticmethod
    def view_all_departments(university: University) -> None:
        """View all departments."""
        if not university.departments:
            print("\nNo departments found in the system.")
            return
        
        print("\n" + "="*70)
        print("ALL DEPARTMENTS")
        print("="*70)
        print(f"{'ID':<8} {'Name':<25} {'Head':<12} {'Courses':<10}")
        print("-"*70)
        
        for department in university.departments:
            print(f"{department.department_id:<8} {department.name:<25} "
                  f"{department.head_of_department if department.head_of_department else 'None':<12} "
                  f"{len(department.courses_offered):<10}")
        
        print("="*70)
        print(f"Total Departments: {len(university.departments)}")
    
    @staticmethod
    def set_head_of_department(university: University) -> None:
        """Set head of department."""
        department_id = input("Enter Department ID: ").strip().upper()
        faculty_id = input("Enter Faculty ID: ").strip()
        
        department = university.find_department(department_id)
        faculty = university.find_faculty(faculty_id)
        
        if not department:
            print(f"⚠ Department {department_id} not found!")
            return
        
        if not faculty:
            print(f"⚠ Faculty {faculty_id} not found!")
            return
        
        if department.set_head_of_department(faculty_id):
            print(f"✓ {faculty.name} set as head of {department.name} department!")
        else:
            print("⚠ Failed to set head of department!")
    
    @staticmethod
    def display_operations_menu(university: University) -> None:
        """Display university operations menu."""
        while True:
            print("\n" + "="*50)
            print("UNIVERSITY OPERATIONS")
            print("="*50)
            print("1. Enroll Student in Course")
            print("2. Assign Faculty to Course")
            print("3. Assign Grade to Student")
            print("4. Set Head of Department")
            print("5. Calculate All GPAs")
            print("0. Back to Main Menu")
            print("="*50)
            
            choice = input("\nEnter your choice (0-5): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                Menu.enroll_student_in_course_menu(university)
            elif choice == '2':
                Menu.assign_faculty_to_course_menu(university)
            elif choice == '3':
                Menu.assign_grade(university)
            elif choice == '4':
                Menu.set_head_of_department(university)
            elif choice == '5':
                university.get_average_gpa()
                print("✓ All GPAs calculated!")
            else:
                print("⚠ Invalid choice! Please try again.")
            
            input("\nPress Enter to continue...")
    
    @staticmethod
    def display_search_menu(university: University) -> None:
        """Display search operations menu."""
        while True:
            print("\n" + "="*50)
            print("SEARCH OPERATIONS")
            print("="*50)
            print("1. Search Students by Name")
            print("2. Search Faculty by Name")
            print("3. Search Courses by Name")
            print("0. Back to Main Menu")
            print("="*50)
            
            choice = input("\nEnter your choice (0-3): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                Menu.search_students_by_name(university)
            elif choice == '2':
                Menu.search_faculty_by_name(university)
            elif choice == '3':
                Menu.search_courses_by_name(university)
            else:
                print("⚠ Invalid choice! Please try again.")
            
            input("\nPress Enter to continue...")
    
    @staticmethod
    def search_students_by_name(university: University) -> None:
        """Search students by name."""
        query = input("Enter student name to search: ").strip()
        
        results = university.search_students_by_name(query)
        
        if not results:
            print(f"No students found with name containing '{query}'")
            return
        
        print(f"\nFound {len(results)} student(s):")
        print("="*70)
        print(f"{'ID':<10} {'Name':<20} {'Department':<15} {'GPA':<6}")
        print("-"*70)
        
        for student in results:
            print(f"{student.student_id:<10} {student.name:<20} "
                  f"{student.department:<15} {student.gpa:<6.2f}")
    
    @staticmethod
    def search_faculty_by_name(university: University) -> None:
        """Search faculty by name."""
        query = input("Enter faculty name to search: ").strip()
        
        results = university.search_faculty_by_name(query)
        
        if not results:
            print(f"No faculty found with name containing '{query}'")
            return
        
        print(f"\nFound {len(results)} faculty member(s):")
        print("="*60)
        print(f"{'ID':<10} {'Name':<20} {'Department':<15}")
        print("-"*60)
        
        for faculty in results:
            print(f"{faculty.faculty_id:<10} {faculty.name:<20} {faculty.department:<15}")
    
    @staticmethod
    def search_courses_by_name(university: University) -> None:
        """Search courses by name."""
        query = input("Enter course name to search: ").strip()
        
        results = university.search_courses_by_name(query)
        
        if not results:
            print(f"No courses found with name containing '{query}'")
            return
        
        print(f"\nFound {len(results)} course(s):")
        print("="*80)
        print(f"{'ID':<10} {'Name':<25} {'Credits':<8} {'Faculty':<12} {'Students':<10}")
        print("-"*80)
        
        for course in results:
            print(f"{course.course_id:<10} {course.name:<25} "
                  f"{course.credit_hours:<8} {course.assigned_faculty if course.assigned_faculty else 'None':<12} "
                  f"{len(course.enrolled_students):<10}")
    
    @staticmethod
    def generate_sample_data(university: University) -> None:
        """Generate sample data for testing."""
        print("\n" + "="*50)
        print("GENERATING SAMPLE DATA")
        print("="*50)
        
        try:
            # Clear existing data first
            university.departments.clear()
            university.faculty.clear()
            university.students.clear()
            university.courses.clear()
            
            # Add sample departments
            departments = [
                ("CSE", "Computer Science & Engineering"),
                ("EEE", "Electrical & Electronics Engineering"),
                ("MAT", "Mathematics"),
                ("PHY", "Physics")
            ]
            
            for dept_id, dept_name in departments:
                department = Department(dept_id, dept_name)
                university.add_department(department)
            
            print("✓ Sample departments added")
            
            # Add sample faculty
            faculty_members = [
                ("F0001", "Dr. Sarah Johnson", "CSE"),
                ("F0002", "Prof. Michael Chen", "CSE"),
                ("F0003", "Dr. Emily Davis", "EEE"),
                ("F0004", "Prof. Robert Wilson", "MAT"),
                ("F0005", "Dr. Lisa Thompson", "PHY")
            ]
            
            for faculty_id, name, department in faculty_members:
                faculty = Faculty(faculty_id, name, department)
                university.add_faculty(faculty)
            
            print("✓ Sample faculty added")
            
            # Set heads of departments
            university.find_department("CSE").set_head_of_department("F0001")
            university.find_department("EEE").set_head_of_department("F0003")
            university.find_department("MAT").set_head_of_department("F0004")
            university.find_department("PHY").set_head_of_department("F0005")
            
            # Add sample courses
            courses = [
                ("CSE101", "Introduction to Programming", 3, "CSE"),
                ("CSE201", "Data Structures", 4, "CSE"),
                ("CSE301", "Algorithms", 4, "CSE"),
                ("EEE101", "Circuit Theory", 3, "EEE"),
                ("MAT101", "Calculus I", 4, "MAT"),
                ("PHY101", "Physics I", 3, "PHY"),
                ("CSE401", "Database Systems", 3, "CSE"),
                ("CSE501", "Machine Learning", 4, "CSE")
            ]
            
            for course_id, name, credits, dept in courses:
                course = Course(course_id, name, credits)
                university.add_course(course)
                
                # Add to department
                department = university.find_department(dept)
                if department:
                    department.add_course(course_id)
            
            print("✓ Sample courses added")
            
            # Assign faculty to courses
            university.assign_faculty_to_course("F0001", "CSE101")
            university.assign_faculty_to_course("F0002", "CSE201")
            university.assign_faculty_to_course("F0001", "CSE301")
            university.assign_faculty_to_course("F0003", "EEE101")
            university.assign_faculty_to_course("F0004", "MAT101")
            university.assign_faculty_to_course("F0005", "PHY101")
            university.assign_faculty_to_course("F0002", "CSE401")
            university.assign_faculty_to_course("F0001", "CSE501")
            
            # Add sample students
            students = [
                ("S0001", "Alice Johnson", 20, "F", "CSE"),
                ("S0002", "Bob Smith", 21, "M", "CSE"),
                ("S0003", "Charlie Brown", 22, "M", "EEE"),
                ("S0004", "Diana Prince", 19, "F", "CSE"),
                ("S0005", "Edward Lee", 20, "M", "MAT"),
                ("S0006", "Fiona Green", 21, "F", "PHY"),
                ("S0007", "George King", 23, "M", "CSE"),
                ("S0008", "Hannah White", 20, "F", "EEE")
            ]
            
            for student_id, name, age, gender, dept in students:
                student = Student(student_id, name, age, gender, dept)
                university.add_student(student)
            
            print("✓ Sample students added")
            
            # Enroll students in courses
            enrollments = [
                ("S0001", "CSE101"), ("S0001", "MAT101"), ("S0001", "PHY101"),
                ("S0002", "CSE101"), ("S0002", "CSE201"), ("S0002", "EEE101"),
                ("S0003", "EEE101"), ("S0003", "MAT101"), ("S0003", "PHY101"),
                ("S0004", "CSE101"), ("S0004", "CSE201"), ("S0004", "CSE301"),
                ("S0005", "MAT101"), ("S0005", "PHY101"), ("S0005", "CSE101"),
                ("S0006", "PHY101"), ("S0006", "MAT101"), ("S0006", "EEE101"),
                ("S0007", "CSE201"), ("S0007", "CSE301"), ("S0007", "CSE401"),
                ("S0008", "EEE101"), ("S0008", "MAT101"), ("S0008", "PHY101")
            ]
            
            for student_id, course_id in enrollments:
                university.enroll_student_in_course(student_id, course_id)
            
            print("✓ Sample enrollments added")
            
            # Assign sample grades
            grades = [
                ("S0001", "CSE101", 3.8), ("S0001", "MAT101", 3.5), ("S0001", "PHY101", 3.2),
                ("S0002", "CSE101", 3.0), ("S0002", "CSE201", 3.3), ("S0002", "EEE101", 2.8),
                ("S0003", "EEE101", 3.7), ("S0003", "MAT101", 3.9), ("S0003", "PHY101", 3.5),
                ("S0004", "CSE101", 4.0), ("S0004", "CSE201", 3.8), ("S0004", "CSE301", 3.6),
                ("S0005", "MAT101", 3.2), ("S0005", "PHY101", 2.9), ("S0005", "CSE101", 3.1),
                ("S0006", "PHY101", 3.8), ("S0006", "MAT101", 3.4), ("S0006", "EEE101", 3.0),
                ("S0007", "CSE201", 3.5), ("S0007", "CSE301", 3.7), ("S0007", "CSE401", 3.9),
                ("S0008", "EEE101", 3.1), ("S0008", "MAT101", 3.3), ("S0008", "PHY101", 3.0)
            ]
            
            for student_id, course_id, grade in grades:
                university.assign_grade(student_id, course_id, grade)
            
            print("✓ Sample grades assigned")
            
            print("\n" + "="*50)
            print("SAMPLE DATA GENERATED SUCCESSFULLY!")
            print("="*50)
            
            # Display statistics
            university.display_university_info()
            
        except Exception as e:
            print(f"⚠ Error generating sample data: {e}")