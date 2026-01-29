#!/usr/bin/env python3
"""
University Management System - Main Entry Point
"""

from university import University
from menu import Menu
from file_handler import FileHandler
import sys

def main():
    """Main function to run the University Management System."""
    
    # Create university instance
    university = University("Tech University", "123 College Ave, Tech City")
    
    # Load existing data
    try:
        FileHandler.load_all_data(university)
        print("✓ Data loaded successfully!")
    except FileNotFoundError:
        print("ℹ No existing data found. Starting with empty system.")
    except Exception as e:
        print(f"⚠ Error loading data: {e}")
    
    # Display welcome message
    print("\n" + "="*50)
    print("      UNIVERSITY MANAGEMENT SYSTEM")
    print("="*50)
    
    # Start the main menu
    try:
        Menu.display_main_menu(university)
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
    except Exception as e:
        print(f"\n⚠ An error occurred: {e}")
    
    # Save data before exiting
    try:
        FileHandler.save_all_data(university)
        print("\n✓ All data saved successfully!")
    except Exception as e:
        print(f"\n⚠ Error saving data: {e}")
    
    print("\nThank you for using University Management System!")
    print("Goodbye!")

if __name__ == "__main__":
    main()