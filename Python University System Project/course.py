"""
Course module for University Management System
"""

from typing import List, Dict

class Course:
    """Represents a course in the university."""
    
    def __init__(self, course_id: str, name: str, credit_hours: int):
        """
        Initialize a new Course.
        
        Args:
            course_id: Unique course identifier (format: CSE101)
            name: Course name
            credit_hours: Number of credit hours
        """
        if not self.is_valid_course_id(course_id):
            raise ValueError(f"Invalid course ID format: {course_id}")
        
        if credit_hours <= 0:
            raise ValueError("Credit hours must be positive")
        
        self.course_id = course_id
        self.name = name
        self.credit_hours = credit_hours
        self.assigned_faculty: str = ""  # Faculty ID
        self.enrolled_students: List[str] = []  # List of student IDs
    
    def assign_faculty(self, faculty_id: str) -> bool:
        """
        Assign faculty to course.
        
        Args:
            faculty_id: Faculty identifier
            
        Returns:
            True if assigned successfully
        """
        self.assigned_faculty = faculty_id
        return True
    
    def enroll_student(self, student_id: str) -> bool:
        """
        Enroll a student in the course.
        
        Args:
            student_id: Student identifier
            
        Returns:
            True if enrolled successfully, False if already enrolled
        """
        if student_id in self.enrolled_students:
            return False
        
        self.enrolled_students.append(student_id)
        return True
    
    def remove_student(self, student_id: str) -> bool:
        """
        Remove a student from the course.
        
        Args:
            student_id: Student identifier
            
        Returns:
            True if removed successfully, False if not enrolled
        """
        if student_id in self.enrolled_students:
            self.enrolled_students.remove(student_id)
            return True
        return False
    
    def is_student_enrolled(self, student_id: str) -> bool:
        """Check if a student is enrolled in the course."""
        return student_id in self.enrolled_students
    
    def get_info(self) -> Dict:
        """Get course information as dictionary."""
        return {
            'course_id': self.course_id,
            'name': self.name,
            'credit_hours': self.credit_hours,
            'assigned_faculty': self.assigned_faculty,
            'enrolled_students': self.enrolled_students
        }
    
    def display_info(self) -> None:
        """Display course information."""
        print("\n" + "="*50)
        print("COURSE INFORMATION")
        print("="*50)
        print(f"Course ID: {self.course_id}")
        print(f"Course Name: {self.name}")
        print(f"Credit Hours: {self.credit_hours}")
        print(f"Assigned Faculty: {self.assigned_faculty if self.assigned_faculty else 'Not assigned'}")
        print(f"Enrolled Students: {len(self.enrolled_students)}")
        
        if self.enrolled_students:
            print("Enrolled Students:")
            for i, student_id in enumerate(self.enrolled_students, 1):
                print(f"  {i}. {student_id}")
    
    @staticmethod
    def is_valid_course_id(course_id: str) -> bool:
        """
        Validate course ID format.
        
        Format: Department code + 3 digits (e.g., CSE101)
        """
        if len(course_id) < 4:
            return False
        # Check if first part is letters and last part is digits
        for i, char in enumerate(course_id):
            if char.isdigit():
                return course_id[i:].isdigit() and len(course_id[i:]) == 3
        return False
    
    def to_dict(self) -> Dict:
        """Convert course to dictionary for serialization."""
        return self.get_info()
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Course':
        """Create Course from dictionary."""
        course = cls(
            data['course_id'],
            data['name'],
            data['credit_hours']
        )
        course.assigned_faculty = data['assigned_faculty']
        course.enrolled_students = data['enrolled_students']
        return course