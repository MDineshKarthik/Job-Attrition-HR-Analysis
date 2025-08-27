import mysql.connector
from datetime import datetime

# -------------------------
# MySQL Connection
# -------------------------
conn = mysql.connector.connect(
    host="127.0.0.1",  # change this to your host
    user="root",       # change this to your username
    password="Dineshkarthik@!",  # change this to your password
    database="hr_analytics"
)
cursor = conn.cursor()

# -------------------------
# Core Functions
# -------------------------
def add_employee():
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    gender = input("Enter Gender: ")
    dept_id = int(input("Enter Department ID: "))
    job_role = input("Enter Job Role: ")
    salary = float(input("Enter Salary: "))
    hire_date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT INTO Employees (Name, Age, Gender, DepartmentID, JobRole, Salary, HireDate) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (name, age, gender, dept_id, job_role, salary, hire_date))
    conn.commit()
    print("✅ Employee Added Successfully!")

def mark_exit():
    emp_id = int(input("Enter Employee ID to mark exit: "))
    exit_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("UPDATE Employees SET ExitDate=%s WHERE EmployeeID=%s", (exit_date, emp_id))
    conn.commit()
    print("✅ Employee Exit Recorded!")

def attrition_by_department():
    query = """
    SELECT d.DepartmentName,
           COUNT(e.EmployeeID) AS Total,
           SUM(CASE WHEN e.ExitDate IS NOT NULL THEN 1 ELSE 0 END) AS Exited,
           ROUND((SUM(CASE WHEN e.ExitDate IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) AS AttritionRate
    FROM Employees e
    JOIN Departments d ON e.DepartmentID = d.DepartmentID
    GROUP BY d.DepartmentName
    """
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    print("\t".join(columns))
    for row in cursor.fetchall():
        print("\t".join(str(item) for item in row))

def average_tenure():
    query = """
    SELECT AVG(TIMESTAMPDIFF(DAY, HireDate, COALESCE(ExitDate, CURDATE())) / 365) AS AvgYears
    FROM Employees
    """
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    result = cursor.fetchone()
    print("\t".join(columns))
    print(str(round(result[0], 2)) if result[0] is not None else "N/A")

def salary_vs_attrition():
    query = """
    SELECT CASE 
             WHEN Salary < 40000 THEN 'Low'
             WHEN Salary BETWEEN 40000 AND 70000 THEN 'Medium'
             ELSE 'High'
           END AS SalaryRange,
           COUNT(*) AS Total,
           SUM(CASE WHEN ExitDate IS NOT NULL THEN 1 ELSE 0 END) AS Exited
    FROM Employees
    GROUP BY SalaryRange
    """
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    print("\t".join(columns))
    for row in cursor.fetchall():
        print("\t".join(str(item) for item in row))

# -------------------------
# CLI Menu
# -------------------------
def menu():
    while True:
        print("\n====== Employee Attrition & HR Analytics ======")
        print("1. Add Employee")
        print("2. Mark Employee Exit")
        print("3. Attrition by Department")
        print("4. Average Tenure")
        print("5. Salary vs Attrition")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            add_employee()
        elif choice == "2":
            mark_exit()
        elif choice == "3":
            attrition_by_department()
        elif choice == "4":
            average_tenure()
        elif choice == "5":
            salary_vs_attrition()
        elif choice == "6":
            break
        else:
            print("❌ Invalid choice, try again!")

# -------------------------
# Run Program
# -------------------------
if __name__ == "__main__":
    menu()
    cursor.close()
    conn.close()
