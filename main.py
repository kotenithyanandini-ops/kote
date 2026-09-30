"""
main.py
-------
Simple menu-driven interface for the Student Management System.
Allows users to add, view, search, update, and delete student records interactively.
"""

from student_management import (
    load_students,
    save_students,
    add_student,
    get_all_students,
    search_student,
    update_student,
    delete_student,
)


def display_menu():
    """Displays the main menu options to the user."""
    print("\n" + "=" * 40)
    print("      STUDENT MANAGEMENT SYSTEM")
    print("=" * 40)
    print("1. Add New Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student Details")
    print("5. Delete Student Record")
    print("6. Exit")
    print("=" * 40)


def print_students_table(student_list):
    """
    Prints a formatted table displaying a list of student records.
    """
    if not student_list:
        print("\nNo student records found.")
        return

    print("\n" + "-" * 60)
    print(f"{'ID':<10} | {'Name':<20} | {'Age':<5} | {'Course':<15}")
    print("-" * 60)
    for student in student_list:
        print(f"{student['id']:<10} | {student['name']:<20} | {student['age']:<5} | {student['course']:<15}")
    print("-" * 60)


def handle_add_student(students):
    """Handles user input for adding a new student."""
    print("\n--- Add New Student ---")
    student_id = input("Enter Student ID: ").strip()
    name = input("Enter Name: ").strip()
    age = input("Enter Age: ").strip()
    course = input("Enter Course: ").strip()

    success, message = add_student(students, student_id, name, age, course)
    print(f"\n[Result] {message}")
    if success:
        save_students(students)


def handle_view_students(students):
    """Handles displaying all student records."""
    print("\n--- All Student Records ---")
    student_list = get_all_students(students)
    print_students_table(student_list)


def handle_search_student(students):
    """Handles searching for student records."""
    print("\n--- Search Student ---")
    search_term = input("Enter Student ID or Name to search: ").strip()
    results = search_student(students, search_term)
    print_students_table(results)


def handle_update_student(students):
    """Handles updating student information."""
    print("\n--- Update Student Details ---")
    student_id = input("Enter Student ID to update: ").strip()

    if student_id not in students:
        print(f"\n[Error] Student ID '{student_id}' not found.")
        return

    current = students[student_id]
    print(f"Current Details -> Name: {current['name']}, Age: {current['age']}, Course: {current['course']}")
    print("(Press Enter to keep current value)")

    new_name = input("Enter New Name: ").strip()
    new_age = input("Enter New Age: ").strip()
    new_course = input("Enter New Course: ").strip()

    success, message = update_student(
        students,
        student_id,
        name=new_name if new_name else None,
        age=new_age if new_age else None,
        course=new_course if new_course else None,
    )
    print(f"\n[Result] {message}")
    if success:
        save_students(students)


def handle_delete_student(students):
    """Handles deleting a student record."""
    print("\n--- Delete Student Record ---")
    student_id = input("Enter Student ID to delete: ").strip()

    confirm = input(f"Are you sure you want to delete student ID '{student_id}'? (y/n): ").strip().lower()
    if confirm != 'y':
        print("\nDeletion cancelled.")
        return

    success, message = delete_student(students, student_id)
    print(f"\n[Result] {message}")
    if success:
        save_students(students)


def main():
    """Main program execution loop."""
    students = load_students()
    print("Welcome to the Student Management System!")

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            handle_add_student(students)
        elif choice == "2":
            handle_view_students(students)
        elif choice == "3":
            handle_search_student(students)
        elif choice == "4":
            handle_update_student(students)
        elif choice == "5":
            handle_delete_student(students)
        elif choice == "6":
            print("\nThank you for using Student Management System. Goodbye!")
            break
        else:
            print("\n[Error] Invalid choice! Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
