"""
File Handler module for University Management System
"""

import json
import os
from typing import Dict
from university import University

class FileHandler:
    """Handles file operations for the University Management System."""
    
    DATA_DIR = "data"
    STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
    FACULTY_FILE = os.path.join(DATA_DIR, "faculty.json")
    COURSES_FILE = os.path.join(DATA_DIR, "courses.json")
    DEPARTMENTS_FILE = os.path.join(DATA_DIR, "departments.json")
    UNIVERSITY_FILE = os.path.join(DATA_DIR, "university.json")
    
    @staticmethod
    def ensure_data_dir() -> None:
        """Ensure the data directory exists."""
        if not os.path.exists(FileHandler.DATA_DIR):
            os.makedirs(FileHandler.DATA_DIR)
    
    @staticmethod
    def save_all_data(university: University) -> None:
        """
        Save all university data to files.
        
        Args:
            university: University object
        """
        FileHandler.ensure_data_dir()
        
        try:
            # Save all data in one file
            all_data = university.get_all_data()
            
            with open(FileHandler.UNIVERSITY_FILE, 'w') as f:
                json.dump(all_data, f, indent=2)
            
            print(f"✓ Data saved to {FileHandler.UNIVERSITY_FILE}")
        except Exception as e:
            print(f"⚠ Error saving data: {e}")
            raise
    
    @staticmethod
    def load_all_data(university: University) -> None:
        """
        Load all university data from files.
        
        Args:
            university: University object to load data into
        """
        if not os.path.exists(FileHandler.UNIVERSITY_FILE):
            # Try loading from individual files (backward compatibility)
            if (os.path.exists(FileHandler.STUDENTS_FILE) and
                os.path.exists(FileHandler.FACULTY_FILE) and
                os.path.exists(FileHandler.COURSES_FILE) and
                os.path.exists(FileHandler.DEPARTMENTS_FILE)):
                
                FileHandler._load_legacy_data(university)
                return
        
        try:
            with open(FileHandler.UNIVERSITY_FILE, 'r') as f:
                all_data = json.load(f)
            
            university.load_all_data(all_data)
            print(f"✓ Data loaded from {FileHandler.UNIVERSITY_FILE}")
        except FileNotFoundError:
            print("ℹ No data file found. Starting fresh.")
        except json.JSONDecodeError as e:
            print(f"⚠ Error reading data file: {e}")
        except Exception as e:
            print(f"⚠ Error loading data: {e}")
            raise
    
    @staticmethod
    def _load_legacy_data(university: University) -> None:
        """Load data from legacy individual files (for backward compatibility)."""
        try:
            # Load departments
            with open(FileHandler.DEPARTMENTS_FILE, 'r') as f:
                departments_data = json.load(f)
                for dept_data in departments_data:
                    university.departments.append(Department.from_dict(dept_data))
            
            # Load faculty
            with open(FileHandler.FACULTY_FILE, 'r') as f:
                faculty_data = json.load(f)
                for faculty_data_item in faculty_data:
                    university.faculty.append(Faculty.from_dict(faculty_data_item))
            
            # Load students
            with open(FileHandler.STUDENTS_FILE, 'r') as f:
                students_data = json.load(f)
                for student_data in students_data:
                    university.students.append(Student.from_dict(student_data))
            
            # Load courses
            with open(FileHandler.COURSES_FILE, 'r') as f:
                courses_data = json.load(f)
                for course_data in courses_data:
                    university.courses.append(Course.from_dict(course_data))
            
            print("✓ Legacy data loaded successfully")
        except Exception as e:
            print(f"⚠ Error loading legacy data: {e}")