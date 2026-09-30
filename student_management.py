"""
student_management.py
---------------------
This module contains core business logic and functions for managing student records in the Student Management System.
Records can be loaded from and saved to a JSON file for persistence.
"""

import json
import os


DATA_FILE = "students.json"


def load_students(filename=DATA_FILE):
    """
    Loads student records from a JSON file.
    Returns a dictionary of students where keys are student IDs (as strings).
    If the file does not exist or is empty, returns an empty dictionary.
    """
    if not os.path.exists(filename):
        return {}

    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_students(students, filename=DATA_FILE):
    """
    Saves the dictionary of student records into a JSON file.
    """
    try:
        with open(filename, "w") as file:
            json.dump(students, file, indent=4)
        return True
    except OSError:
        return False


def add_student(students, student_id, name, age, course):
    """
    Adds a new student to the records.

    Parameters:
        students (dict): Dictionary storing current student records.
        student_id (str): Unique identifier for the student.
        name (str): Full name of the student.
        age (int): Age of the student.
        course (str): Course/Major of the student.

    Returns:
        tuple: (success (bool), message (str))
    """
    student_id = str(student_id).strip()

    if not student_id:
        return False, "Student ID cannot be empty."

    if student_id in students:
        return False, f"Student ID '{student_id}' already exists."

    if not name or not name.strip():
        return False, "Student name cannot be empty."

    try:
        age = int(age)
        if age <= 0:
            return False, "Age must be a positive integer."
    except (ValueError, TypeError):
        return False, "Age must be a valid integer."

    if not course or not course.strip():
        return False, "Course cannot be empty."

    students[student_id] = {
        "id": student_id,
        "name": name.strip(),
        "age": age,
        "course": course.strip()
    }

    return True, f"Student '{name.strip()}' added successfully!"


def get_all_students(students):
    """
    Returns a list of all student records.
    """
    return list(students.values())


def search_student(students, search_term):
    """
    Searches for students matching the search_term (matches ID or Name, case-insensitive).

    Parameters:
        students (dict): Dictionary storing student records.
        search_term (str): Search string (ID or name keyword).

    Returns:
        list: List of matching student dictionaries.
    """
    search_term = str(search_term).strip().lower()
    if not search_term:
        return []

    results = []
    for student_id, details in students.items():
        if search_term == student_id.lower() or search_term in details["name"].lower():
            results.append(details)

    return results


def update_student(students, student_id, name=None, age=None, course=None):
    """
    Updates details of an existing student.
    Only updates fields that are provided (not None or empty string).

    Returns:
        tuple: (success (bool), message (str))
    """
    student_id = str(student_id).strip()
    if student_id not in students:
        return False, f"Student ID '{student_id}' not found."

    student = students[student_id]

    if name is not None and name.strip() != "":
        student["name"] = name.strip()

    if age is not None and str(age).strip() != "":
        try:
            valid_age = int(age)
            if valid_age <= 0:
                return False, "Age must be a positive integer."
            student["age"] = valid_age
        except (ValueError, TypeError):
            return False, "Age must be a valid integer."

    if course is not None and course.strip() != "":
        student["course"] = course.strip()

    return True, f"Student ID '{student_id}' updated successfully!"


def delete_student(students, student_id):
    """
    Deletes a student record by ID.

    Returns:
        tuple: (success (bool), message (str))
    """
    student_id = str(student_id).strip()
    if student_id not in students:
        return False, f"Student ID '{student_id}' not found."

    removed_student = students.pop(student_id)
    return True, f"Student '{removed_student['name']}' (ID: {student_id}) deleted successfully!"
