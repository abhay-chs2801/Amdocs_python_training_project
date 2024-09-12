import mysql.connector
from dotenv import load_dotenv
import os
from tabulate import tabulate  # Import tabulate for tabular display

load_dotenv()

# Connect to the MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="EmployeeDB"
    )

# Create a new employee record
def register_employee():
    conn = connect_db()
    cursor = conn.cursor()
    name = input("\nEnter Employee Name: ")
    address = input("Enter Employee Address: ")
    contact_no = input("Enter Employee Contact No: ")
    email = input("Enter Employee Email: ")
    dob = input("Enter Employee DOB (YYYY-MM-DD): ")
    salary = input("Enter Employee Salary: ")
    designation = input("Enter Employee Designation: ")
    gender = input("Enter Employee Gender: ")

    query = """INSERT INTO employees (EmployeeName, EmployeeAddress, EmployeeContactNo, 
              email, dob, salary, designation, gender) 
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (name, address, contact_no, email, dob, salary, designation, gender)
    cursor.execute(query, values)
    conn.commit()
    print(f"\nEmployee {name} registered successfully!")
    conn.close()

# Admin authentication function
def authenticate_admin():
    conn = connect_db()
    cursor = conn.cursor()
    username = input("Enter Admin Username: ")
    password = input("Enter Admin Password: ")

    query = "SELECT * FROM admin WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        print(f"Welcome, {username}!")
        conn.close()
        return True
    else:
        print("Invalid username or password.")
        conn.close()
        return False
    
# Read all employees and display them in tabular format
def read_all_employees():
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM employees"
    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        headers = ["ID", "Name", "Address", "Contact", "Email", "DOB", "Salary", "Designation", "Gender"]
        print(tabulate(result, headers=headers, tablefmt="pretty"))
    else:
        print("\nNo employees found in the database.")
    
    conn.close()

# Read a specific employee by ID and display it in tabular format
def read_employee_by_id():
    conn = connect_db()
    cursor = conn.cursor()
    emp_id = input("\nEnter Employee ID: ")
    query = "SELECT * FROM employees WHERE EmployeeId = %s"
    cursor.execute(query, (emp_id,))
    result = cursor.fetchone()

    if result:
        headers = ["ID", "Name", "Address", "Contact", "Email", "DOB", "Salary", "Designation", "Gender"]
        print(tabulate([result], headers=headers, tablefmt="pretty"))
    else:
        print(f"\nEmployee with ID {emp_id} not found.")
    
    conn.close()

# Update employee details (Preserve original values for empty fields)
def update_employee():
    conn = connect_db()
    cursor = conn.cursor()
    emp_id = input("\nEnter Employee ID to update: ")

    query = "SELECT * FROM employees WHERE EmployeeId = %s"
    cursor.execute(query, (emp_id,))
    result = cursor.fetchone()

    if result:
        print("\nPress Enter if you do not want to change a field.")
        name = input(f"Enter new Employee Name [{result[1]}]: ") or result[1]
        address = input(f"Enter new Employee Address [{result[2]}]: ") or result[2]
        contact_no = input(f"Enter new Employee Contact No [{result[3]}]: ") or result[3]
        email = input(f"Enter new Employee Email [{result[4]}]: ") or result[4]
        dob = input(f"Enter new Employee DOB (YYYY-MM-DD) [{result[5]}]: ") or result[5]
        salary = input(f"Enter new Employee Salary [{result[6]}]: ") or result[6]
        designation = input(f"Enter new Employee Designation [{result[7]}]: ") or result[7]
        gender = input(f"Enter new Employee Gender [{result[8]}]: ") or result[8]

        query = """UPDATE employees SET EmployeeName = %s, EmployeeAddress = %s, EmployeeContactNo = %s, 
                   email= %s, dob = %s, salary = %s, designation = %s, gender = %s 
                   WHERE EmployeeId = %s"""
        values = (name, address, contact_no, email, dob, salary, designation, gender, emp_id)
        cursor.execute(query, values)
        conn.commit()
        print(f"\nEmployee {emp_id} updated successfully!")
    else:
        print(f"\nEmployee with ID {emp_id} not found.")
    
    conn.close()

# Delete employee
def delete_employee():
    conn = connect_db()
    cursor = conn.cursor()
    emp_id = input("\nEnter Employee ID to delete: ")
    query = "SELECT * FROM employees WHERE EmployeeId = %s"
    cursor.execute(query, (emp_id,))
    result = cursor.fetchone()

    if result:
        delete_query = "DELETE FROM employees WHERE EmployeeId = %s"
        cursor.execute(delete_query, (emp_id,))
        conn.commit()
        print(f"\nEmployee {emp_id} deleted successfully!")
    else:
        print(f"\nEmployee with ID {emp_id} not found.")
    
    conn.close()

# Main function to run the application
def main():
    if authenticate_admin():
        while True:
            print("\nEmployee Management System")
            print("1. Register New Employee")
            print("2. View All Employees")
            print("3. View Employee by ID")
            print("4. Update Employee")
            print("5. Delete Employee")
            print("6. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                register_employee()
            elif choice == '2':
                read_all_employees()
            elif choice == '3':
                read_employee_by_id()
            elif choice == '4':
                update_employee()
            elif choice == '5':
                delete_employee()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Access Denied!")

if __name__ == "__main__":
    main()
