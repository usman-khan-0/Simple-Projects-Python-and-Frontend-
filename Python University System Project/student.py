"""
Student module for University Management System
"""

from typing import Dict, List, Optional
import json

class Student:
    """Represents a student in the university."""
    
    def __init__(self, student_id: str, name: str, age: int, 
                 gender: str, department: str):
        """
        Initialize a new Student.
        
        Args:
            student_id: Unique student identifier (format: S0000)
            name: Student's full name
            age: Student's age
            gender: Student's gender
            department: Department name
        """
        if not self.is_valid_student_id(student_id):
            raise ValueError(f"Invalid student ID format: {student_id}")
        
        self.student_id = student_id
        self.name = name
        self.age = age
        self.gender = gender
        self.department = department
        self.course_grades: Dict[str, float] = {}  # course_id -> grade (0.0-4.0)
        self.gpa = 0.0
        
        self._calculate_gpa()
    
    def _calculate_gpa(self) -> None:
        """Calculate GPA based on course grades."""
        if not self.course_grades:
            self.gpa = 0.0
            return
        
        total_points = sum(self.course_grades.values())
        self.gpa = total_points / len(self.course_grades)
    
    def enroll_in_course(self, course_id: str) -> bool:
        """
        Enroll student in a course.
        
        Args:
            course_id: Course identifier
            
        Returns:
            True if enrolled successfully, False if already enrolled
        """
        if course_id in self.course_grades:
            return False
        
        self.course_grades[course_id] = 0.0  # Initialize with 0 grade
        return True
    
    def assign_grade(self, course_id: str, grade: float) -> bool:
        """
        Assign a grade for a course.
        
        Args:
            course_id: Course identifier
            grade: Grade value (0.0-4.0)
            
        Returns:
            True if grade assigned successfully, False otherwise
        """
        if course_id not in self.course_grades:
            return False
        
        if not 0.0 <= grade <= 4.0:
            return False
        
        self.course_grades[course_id] = grade
        self._calculate_gpa()
        return True
    
    def drop_course(self, course_id: str) -> bool:
        """
        Drop a course.
        
        Args:
            course_id: Course identifier
            
        Returns:
            True if dropped successfully, False if not enrolled
        """
        if course_id in self.course_grades:
            del self.course_grades[course_id]
            self._calculate_gpa()
            return True
        return False
    
    def is_enrolled_in_course(self, course_id: str) -> bool:
        """Check if student is enrolled in a course."""
        return course_id in self.course_grades
    
    def get_info(self) -> Dict:
        """Get student information as dictionary."""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'department': self.department,
            'gpa': self.gpa,
            'course_grades': self.course_grades
        }
    
    def display_info(self) -> None:
        """Display student information."""
        print("\n" + "="*50)
        print("STUDENT INFORMATION")
        print("="*50)
        print(f"Student ID: {self.student_id}")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Gender: {self.gender}")
        print(f"Department: {self.department}")
        print(f"GPA: {self.gpa:.2f}")
        print(f"Courses Enrolled: {len(self.course_grades)}")
    
    def display_course_grades(self) -> None:
        """Display all course grades."""
        if not self.course_grades:
            print("No courses enrolled.")
            return
        
        print("\n" + "-"*40)
        print(f"COURSE GRADES - {self.name}")
        print("-"*40)
        print(f"{'Course ID':<15} {'Grade':<10}")
        print("-"*40)
        
        for course_id, grade in self.course_grades.items():
            print(f"{course_id:<15} {grade:<10.2f}")
    
    @staticmethod
    def is_valid_student_id(student_id: str) -> bool:
        """
        Validate student ID format.
        
        Format: S followed by 4 digits (e.g., S0001)
        """
        if len(student_id) != 5:
            return False
        if student_id[0] != 'S':
            return False
        return student_id[1:].isdigit()
    
    def to_dict(self) -> Dict:
        """Convert student to dictionary for serialization."""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'department': self.department,
            'gpa': self.gpa,
            'course_grades': self.course_grades
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Student':
        """Create Student from dictionary."""
        student = cls(
            data['student_id'],
            data['name'],
            data['age'],
            data['gender'],
            data['department']
        )
        student.gpa = data['gpa']
        student.course_grades = data['course_grades']
        return student