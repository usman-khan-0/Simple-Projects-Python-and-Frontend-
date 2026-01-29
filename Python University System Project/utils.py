"""
Utility functions for University Management System
"""

import os
import sys
from typing import Any, List

def clear_screen() -> None:
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title: str) -> None:
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"{title:^60}")
    print("="*60)

def get_valid_input(prompt: str, validation_func, error_msg: str = "Invalid input!") -> Any:
    """
    Get valid input from user with validation.
    
    Args:
        prompt: Input prompt
        validation_func: Function to validate input
        error_msg: Error message for invalid input
        
    Returns:
        Validated input
    """
    while True:
        try:
            value = input(prompt).strip()
            if validation_func(value):
                return value
            else:
                print(f"⚠ {error_msg}")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            sys.exit(0)
        except Exception as e:
            print(f"⚠ Error: {e}")

def format_table(headers: List[str], data: List[List[str]], 
                 col_widths: List[int] = None) -> str:
    """
    Format data as a table.
    
    Args:
        headers: List of header strings
        data: List of rows (each row is a list of strings)
        col_widths: List of column widths (optional)
        
    Returns:
        Formatted table as string
    """
    if col_widths is None:
        col_widths = [len(h) + 2 for h in headers]
    
    # Build header
    table = "  ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths)) + "\n"
    table += "-" * (sum(col_widths) + (len(headers) - 1) * 2) + "\n"
    
    # Build rows
    for row in data:
        table += "  ".join(f"{cell:<{w}}" for cell, w in zip(row, col_widths)) + "\n"
    
    return table

def confirm_action(prompt: str) -> bool:
    """
    Ask for confirmation before performing an action.
    
    Args:
        prompt: Confirmation prompt
        
    Returns:
        True if confirmed, False otherwise
    """
    response = input(f"{prompt} (yes/no): ").strip().lower()
    return response in ['yes', 'y']