"""
Faculty module for University Management System
"""

from typing import List, Dict

class Faculty:
    """Represents a faculty member in the university."""
    
    def __init__(self, faculty_id: str, name: str, department: str):
        """
        Initialize a new Faculty member.
        
        Args:
            faculty_id: Unique faculty identifier (format: F0000)
            name: Faculty's full name
            department: Department name
        """
        if not self.is_valid_faculty_id(faculty_id):
            raise ValueError(f"Invalid faculty ID format: {faculty_id}")
        
        self.faculty_id = faculty_id
        self.name = name
        self.department = department
        self.courses_taught: List[str] = []  # List of course IDs
    
    def assign_course(self, course_id: str) -> bool:
        """
        Assign a course to faculty.
        
        Args:
            course_id: Course identifier
            
        Returns:
            True if assigned successfully, False if already teaching
        """
        if course_id in self.courses_taught:
            return False
        
        self.courses_taught.append(course_id)
        return True
    
    def remove_course(self, course_id: str) -> bool:
        """
        Remove a course from faculty.
        
        Args:
            course_id: Course identifier
            
        Returns:
            True if removed successfully, False if not teaching
        """
        if course_id in self.courses_taught:
            self.courses_taught.remove(course_id)
            return True
        return False
    
    def is_teaching_course(self, course_id: str) -> bool:
        """Check if faculty is teaching a course."""
        return course_id in self.courses_taught
    
    def get_info(self) -> Dict:
        """Get faculty information as dictionary."""
        return {
            'faculty_id': self.faculty_id,
            'name': self.name,
            'department': self.department,
            'courses_taught': self.courses_taught
        }
    
    def display_info(self) -> None:
        """Display faculty information."""
        print("\n" + "="*50)
        print("FACULTY INFORMATION")
        print("="*50)
        print(f"Faculty ID: {self.faculty_id}")
        print(f"Name: {self.name}")
        print(f"Department: {self.department}")
        print(f"Courses Taught: {len(self.courses_taught)}")
        
        if self.courses_taught:
            print("Courses:")
            for course_id in self.courses_taught:
                print(f"  - {course_id}")
    
    @staticmethod
    def is_valid_faculty_id(faculty_id: str) -> bool:
        """
        Validate faculty ID format.
        
        Format: F followed by 4 digits (e.g., F0001)
        """
        if len(faculty_id) != 5:
            return False
        if faculty_id[0] != 'F':
            return False
        return faculty_id[1:].isdigit()
    
    def to_dict(self) -> Dict:
        """Convert faculty to dictionary for serialization."""
        return self.get_info()
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Faculty':
        """Create Faculty from dictionary."""
        faculty = cls(
            data['faculty_id'],
            data['name'],
            data['department']
        )
        faculty.courses_taught = data['courses_taught']
        return faculty