"""
Department module for University Management System
"""

from typing import List, Dict

class Department:
    """Represents a department in the university."""
    
    def __init__(self, department_id: str, name: str):
        """
        Initialize a new Department.
        
        Args:
            department_id: Unique department identifier (format: CSE)
            name: Department name
        """
        if not self.is_valid_department_id(department_id):
            raise ValueError(f"Invalid department ID format: {department_id}")
        
        self.department_id = department_id
        self.name = name
        self.head_of_department: str = ""  # Faculty ID
        self.courses_offered: List[str] = []  # List of course IDs
    
    def set_head_of_department(self, faculty_id: str) -> bool:
        """
        Set head of department.
        
        Args:
            faculty_id: Faculty identifier
            
        Returns:
            True if set successfully
        """
        self.head_of_department = faculty_id
        return True
    
    def add_course(self, course_id: str) -> bool:
        """
        Add a course to department.
        
        Args:
            course_id: Course identifier
            
        Returns:
            True if added successfully, False if already offered
        """
        if course_id in self.courses_offered:
            return False
        
        self.courses_offered.append(course_id)
        return True
    
    def remove_course(self, course_id: str) -> bool:
        """
        Remove a course from department.
        
        Args:
            course_id: Course identifier
            
        Returns:
            True if removed successfully, False if not offered
        """
        if course_id in self.courses_offered:
            self.courses_offered.remove(course_id)
            return True
        return False
    
    def offers_course(self, course_id: str) -> bool:
        """Check if department offers a course."""
        return course_id in self.courses_offered
    
    def get_info(self) -> Dict:
        """Get department information as dictionary."""
        return {
            'department_id': self.department_id,
            'name': self.name,
            'head_of_department': self.head_of_department,
            'courses_offered': self.courses_offered
        }
    
    def display_info(self) -> None:
        """Display department information."""
        print("\n" + "="*50)
        print("DEPARTMENT INFORMATION")
        print("="*50)
        print(f"Department ID: {self.department_id}")
        print(f"Department Name: {self.name}")
        print(f"Head of Department: {self.head_of_department if self.head_of_department else 'Not assigned'}")
        print(f"Courses Offered: {len(self.courses_offered)}")
        
        if self.courses_offered:
            print("Courses Offered:")
            for i, course_id in enumerate(self.courses_offered, 1):
                print(f"  {i}. {course_id}")
    
    @staticmethod
    def is_valid_department_id(department_id: str) -> bool:
        """
        Validate department ID format.
        
        Format: 2-4 uppercase letters (e.g., CSE, MATH, PHY)
        """
        if len(department_id) < 2 or len(department_id) > 4:
            return False
        return department_id.isalpha() and department_id.isupper()
    
    def to_dict(self) -> Dict:
        """Convert department to dictionary for serialization."""
        return self.get_info()
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Department':
        """Create Department from dictionary."""
        department = cls(
            data['department_id'],
            data['name']
        )
        department.head_of_department = data['head_of_department']
        department.courses_offered = data['courses_offered']
        return department