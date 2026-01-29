"""
University module for University Management System
"""

from typing import List, Dict, Optional
from student import Student
from faculty import Faculty
from course import Course
from department import Department

class University:
    """Represents the university and manages all entities."""
    
    def __init__(self, name: str = "Tech University", 
                 address: str = "123 College Ave, Tech City"):
        """
        Initialize the University.
        
        Args:
            name: University name
            address: University address
        """
        self.name = name
        self.address = address
        self.departments: List[Department] = []
        self.students: List[Student] = []
        self.faculty: List[Faculty] = []
        self.courses: List[Course] = []
    
    def add_student(self, student: Student) -> bool:
        """
        Add a student to the university.
        
        Args:
            student: Student object
            
        Returns:
            True if added successfully, False if student ID already exists
        """
        if self.find_student(student.student_id):
            return False
        
        self.students.append(student)
        return True
    
    def add_faculty(self, faculty_member: Faculty) -> bool:
        """
        Add a faculty member to the university.
        
        Args:
            faculty_member: Faculty object
            
        Returns:
            True if added successfully, False if faculty ID already exists
        """
        if self.find_faculty(faculty_member.faculty_id):
            return False
        
        self.faculty.append(faculty_member)
        return True
    
    def add_course(self, course: Course) -> bool:
        """
        Add a course to the university.
        
        Args:
            course: Course object
            
        Returns:
            True if added successfully, False if course ID already exists
        """
        if self.find_course(course.course_id):
            return False
        
        self.courses.append(course)
        return True
    
    def add_department(self, department: Department) -> bool:
        """
        Add a department to the university.
        
        Args:
            department: Department object
            
        Returns:
            True if added successfully, False if department ID already exists
        """
        if self.find_department(department.department_id):
            return False
        
        self.departments.append(department)
        return True
    
    def remove_student(self, student_id: str) -> bool:
        """
        Remove a student from the university.
        
        Args:
            student_id: Student identifier
            
        Returns:
            True if removed successfully, False if student not found
        """
        student = self.find_student(student_id)
        if student:
            self.students.remove(student)
            
            # Remove student from all courses
            for course in self.courses:
                course.remove_student(student_id)
            
            return True
        return False
    
    def remove_faculty(self, faculty_id: str) -> bool:
        """
        Remove a faculty member from the university.
        
        Args:
            faculty_id: Faculty identifier
            
        Returns:
            True if removed successfully, False if faculty not found
        """
        faculty_member = self.find_faculty(faculty_id)
        if faculty_member:
            self.faculty.remove(faculty_member)
            
            # Remove faculty from courses they were teaching
            for course in self.courses:
                if course.assigned_faculty == faculty_id:
                    course.assigned_faculty = ""
            
            # Remove as head of department
            for department in self.departments:
                if department.head_of_department == faculty_id:
                    department.head_of_department = ""
            
            return True
        return False
    
    def remove_course(self, course_id: str) -> bool:
        """
        Remove a course from the university.
        
        Args:
            course_id: Course identifier
            
        Returns:
            True if removed successfully, False if course not found
        """
        course = self.find_course(course_id)
        if course:
            self.courses.remove(course)
            
            # Remove course from students' enrollments
            for student in self.students:
                student.drop_course(course_id)
            
            # Remove course from faculty teaching assignments
            for faculty_member in self.faculty:
                faculty_member.remove_course(course_id)
            
            # Remove course from departments
            for department in self.departments:
                department.remove_course(course_id)
            
            return True
        return False
    
    def remove_department(self, department_id: str) -> bool:
        """
        Remove a department from the university.
        
        Args:
            department_id: Department identifier
            
        Returns:
            True if removed successfully, False if department not found
        """
        department = self.find_department(department_id)
        if department:
            self.departments.remove(department)
            return True
        return False
    
    def find_student(self, student_id: str) -> Optional[Student]:
        """Find a student by ID."""
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None
    
    def find_faculty(self, faculty_id: str) -> Optional[Faculty]:
        """Find a faculty member by ID."""
        for faculty_member in self.faculty:
            if faculty_member.faculty_id == faculty_id:
                return faculty_member
        return None
    
    def find_course(self, course_id: str) -> Optional[Course]:
        """Find a course by ID."""
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None
    
    def find_department(self, department_id: str) -> Optional[Department]:
        """Find a department by ID."""
        for department in self.departments:
            if department.department_id == department_id:
                return department
        return None
    
    def search_students_by_name(self, name_query: str) -> List[Student]:
        """Search students by name (case-insensitive partial match)."""
        name_query = name_query.lower()
        return [s for s in self.students if name_query in s.name.lower()]
    
    def search_faculty_by_name(self, name_query: str) -> List[Faculty]:
        """Search faculty by name (case-insensitive partial match)."""
        name_query = name_query.lower()
        return [f for f in self.faculty if name_query in f.name.lower()]
    
    def search_courses_by_name(self, name_query: str) -> List[Course]:
        """Search courses by name (case-insensitive partial match)."""
        name_query = name_query.lower()
        return [c for c in self.courses if name_query in c.name.lower()]
    
    def enroll_student_in_course(self, student_id: str, course_id: str) -> bool:
        """
        Enroll a student in a course.
        
        Args:
            student_id: Student identifier
            course_id: Course identifier
            
        Returns:
            True if enrolled successfully, False otherwise
        """
        student = self.find_student(student_id)
        course = self.find_course(course_id)
        
        if not student or not course:
            return False
        
        # Enroll student in course
        if course.enroll_student(student_id):
            # Add course to student's enrollments
            return student.enroll_in_course(course_id)
        
        return False
    
    def assign_faculty_to_course(self, faculty_id: str, course_id: str) -> bool:
        """
        Assign a faculty member to teach a course.
        
        Args:
            faculty_id: Faculty identifier
            course_id: Course identifier
            
        Returns:
            True if assigned successfully, False otherwise
        """
        faculty_member = self.find_faculty(faculty_id)
        course = self.find_course(course_id)
        
        if not faculty_member or not course:
            return False
        
        # Assign faculty to course
        if course.assign_faculty(faculty_id):
            # Add course to faculty's teaching assignments
            return faculty_member.assign_course(course_id)
        
        return False
    
    def assign_grade(self, student_id: str, course_id: str, grade: float) -> bool:
        """
        Assign a grade to a student for a course.
        
        Args:
            student_id: Student identifier
            course_id: Course identifier
            grade: Grade value (0.0-4.0)
            
        Returns:
            True if grade assigned successfully, False otherwise
        """
        student = self.find_student(student_id)
        if not student:
            return False
        
        return student.assign_grade(course_id, grade)
    
    def get_university_stats(self) -> Dict:
        """Get university statistics."""
        return {
            'name': self.name,
            'address': self.address,
            'total_students': len(self.students),
            'total_faculty': len(self.faculty),
            'total_courses': len(self.courses),
            'total_departments': len(self.departments),
            'average_gpa': self.get_average_gpa()
        }
    
    def get_average_gpa(self) -> float:
        """Calculate average GPA of all students."""
        if not self.students:
            return 0.0
        
        total_gpa = sum(student.gpa for student in self.students)
        return total_gpa / len(self.students)
    
    def sort_students_by_gpa(self, descending: bool = True) -> List[Student]:
        """Sort students by GPA."""
        return sorted(self.students, 
                     key=lambda s: s.gpa, 
                     reverse=descending)
    
    def display_university_info(self) -> None:
        """Display university information and statistics."""
        print("\n" + "="*60)
        print(f"UNIVERSITY: {self.name}")
        print("="*60)
        print(f"Address: {self.address}")
        print(f"Departments: {len(self.departments)}")
        print(f"Faculty Members: {len(self.faculty)}")
        print(f"Students: {len(self.students)}")
        print(f"Courses Offered: {len(self.courses)}")
        print(f"Average GPA: {self.get_average_gpa():.2f}")
        print("="*60)
    
    def display_detailed_stats(self) -> None:
        """Display detailed university statistics."""
        self.display_university_info()
        
        print("\nDEPARTMENT WISE STATISTICS:")
        print("-"*60)
        print(f"{'Department':<20} {'Students':<10} {'Faculty':<10} {'Courses':<10}")
        print("-"*60)
        
        for department in self.departments:
            dept_students = len([s for s in self.students if s.department == department.department_id])
            dept_faculty = len([f for f in self.faculty if f.department == department.department_id])
            print(f"{department.name:<20} {dept_students:<10} {dept_faculty:<10} {len(department.courses_offered):<10}")
    
    def get_all_data(self) -> Dict:
        """Get all university data as dictionary for serialization."""
        return {
            'name': self.name,
            'address': self.address,
            'departments': [dept.to_dict() for dept in self.departments],
            'students': [student.to_dict() for student in self.students],
            'faculty': [faculty.to_dict() for faculty in self.faculty],
            'courses': [course.to_dict() for course in self.courses]
        }
    
    def load_all_data(self, data: Dict) -> None:
        """Load all university data from dictionary."""
        self.name = data.get('name', self.name)
        self.address = data.get('address', self.address)
        
        # Clear existing data
        self.departments.clear()
        self.students.clear()
        self.faculty.clear()
        self.courses.clear()
        
        # Load departments
        for dept_data in data.get('departments', []):
            self.departments.append(Department.from_dict(dept_data))
        
        # Load faculty
        for faculty_data in data.get('faculty', []):
            self.faculty.append(Faculty.from_dict(faculty_data))
        
        # Load students
        for student_data in data.get('students', []):
            self.students.append(Student.from_dict(student_data))
        
        # Load courses
        for course_data in data.get('courses', []):
            self.courses.append(Course.from_dict(course_data))