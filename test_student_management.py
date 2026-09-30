"""
test_student_management.py
---------------------------
Unit tests for the Student Management System.
Tests core functions in student_management.py: add, view, search, update, delete, and file persistence.
"""

import os
import json
import unittest

from student_management import (
    load_students,
    save_students,
    add_student,
    get_all_students,
    search_student,
    update_student,
    delete_student,
)


class TestStudentManagement(unittest.TestCase):
    def setUp(self):
        """Set up an isolated student dictionary and test filename before each test."""
        self.students = {}
        self.test_file = "test_students.json"

    def tearDown(self):
        """Clean up test file if created during test."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_student_success(self):
        success, msg = add_student(self.students, "101", "Alice Smith", 20, "Computer Science")
        self.assertTrue(success)
        self.assertIn("101", self.students)
        self.assertEqual(self.students["101"]["name"], "Alice Smith")
        self.assertEqual(self.students["101"]["age"], 20)
        self.assertEqual(self.students["101"]["course"], "Computer Science")

    def test_add_student_duplicate_id(self):
        add_student(self.students, "101", "Alice Smith", 20, "Computer Science")
        success, msg = add_student(self.students, "101", "Bob Brown", 22, "Mathematics")
        self.assertFalse(success)
        self.assertIn("already exists", msg)

    def test_add_student_invalid_inputs(self):
        # Empty ID
        success, _ = add_student(self.students, "", "Alice", 20, "CS")
        self.assertFalse(success)

        # Empty Name
        success, _ = add_student(self.students, "102", "   ", 20, "CS")
        self.assertFalse(success)

        # Invalid Age (string non-numeric)
        success, _ = add_student(self.students, "102", "Bob", "invalid_age", "CS")
        self.assertFalse(success)

        # Negative Age
        success, _ = add_student(self.students, "102", "Bob", -5, "CS")
        self.assertFalse(success)

        # Empty Course
        success, _ = add_student(self.students, "102", "Bob", 20, "")
        self.assertFalse(success)

    def test_get_all_students(self):
        add_student(self.students, "101", "Alice", 20, "CS")
        add_student(self.students, "102", "Bob", 22, "Math")
        all_students = get_all_students(self.students)
        self.assertEqual(len(all_students), 2)

    def test_search_student(self):
        add_student(self.students, "101", "Alice Smith", 20, "CS")
        add_student(self.students, "102", "Bob Johnson", 22, "Math")

        # Search by exact ID
        results = search_student(self.students, "101")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Alice Smith")

        # Search by partial name (case insensitive)
        results = search_student(self.students, "john")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "102")

        # Search non-existing
        results = search_student(self.students, "NonExistent")
        self.assertEqual(len(results), 0)

    def test_update_student_success(self):
        add_student(self.students, "101", "Alice Smith", 20, "CS")

        # Update name and age only
        success, msg = update_student(self.students, "101", name="Alice Jones", age=21)
        self.assertTrue(success)
        self.assertEqual(self.students["101"]["name"], "Alice Jones")
        self.assertEqual(self.students["101"]["age"], 21)
        self.assertEqual(self.students["101"]["course"], "CS")

    def test_update_student_not_found(self):
        success, msg = update_student(self.students, "999", name="New Name")
        self.assertFalse(success)
        self.assertIn("not found", msg)

    def test_update_student_invalid_age(self):
        add_student(self.students, "101", "Alice Smith", 20, "CS")
        success, msg = update_student(self.students, "101", age="invalid")
        self.assertFalse(success)

    def test_delete_student_success(self):
        add_student(self.students, "101", "Alice Smith", 20, "CS")
        success, msg = delete_student(self.students, "101")
        self.assertTrue(success)
        self.assertNotIn("101", self.students)

    def test_delete_student_not_found(self):
        success, msg = delete_student(self.students, "999")
        self.assertFalse(success)

    def test_load_and_save_students(self):
        add_student(self.students, "101", "Alice Smith", 20, "CS")
        saved = save_students(self.students, filename=self.test_file)
        self.assertTrue(saved)

        loaded_students = load_students(filename=self.test_file)
        self.assertEqual(loaded_students, self.students)


if __name__ == "__main__":
    unittest.main()
