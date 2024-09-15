import sqlite3
from datetime import datetime, timedelta
import csv

# Connect to the SQLite database
conn = sqlite3.connect('my_classes.db')
cursor = conn.cursor()

# Get the current date
date = datetime.now().date()
view_or_edit=int(input("""view or edit?
                       1 - view
                       2 - edit """))
if view_or_edit==1:
    # Execute the query
    cursor.execute("""
    SELECT Students.name, Payments.payment_date, Payments.number_of_classes
    FROM Payments
    JOIN Students ON Payments.student_id = Students.id
    ORDER BY Payments.payment_date;
""")

# Fetch all results
    payments = cursor.fetchall()

# Display the results
    for payment in payments:
        print(f"{payment[0]}, {payment[1]}, classes: {payment[2]}")
    conn.close()
# Close the connection

if view_or_edit==2:
    while True:
    # Fetch subject names and IDs from the Subjects table
        cursor.execute("SELECT id, subject_name FROM Subjects")
        subjects = cursor.fetchall()
        # Display the list of subjects
        print("Subjects:")
        for subject in subjects:
            print(f"{subject[0]}: {subject[1]}")

# Input the subject ID, student ID, date, and notes from the user
        subject_id=input("Select a subject ID by typing a number: ")
        cursor.execute("SELECT id, name FROM Students WHERE Subject_id=?", (subject_id,))
        students = cursor.fetchall()
    # Display the list of students
        print("Students:")
        for student in students:
            print(f"{student[0]}: {student[1]}")
        student_id = int(input("Enter the student ID: "))
        date = int(input("Enter the date: 1: today 2: yesterday 3:another date "))
        if date == int(1):
            date = str(datetime.now().date())
        elif date == int(2):
            date = str(datetime.now().date() - timedelta(days=1))
        elif date == int(3):
            date = '2024-' + str(input("Enter the date in MM-DD format: "))

# Convert the string to a datetime object
        date_obj = datetime.strptime(date, "%Y-%m-%d")

# Format the date to DD-Month day of the week
        formatted_date = date_obj.strftime("%d-%B %A")

        print(formatted_date)  # Output: 09-June Friday

        if student_id in [11,12,13,14,15]:
            number_of_classes = 1
        else:
            number_of_classes=int(input("How many classes? "))


        payment_type = input("Payment method: ")
        print(f'Student - {student_id}, {date}, paymment of {number_of_classes} classes, method - {payment_type}')
        answer=int(input("all good? 1 - yes, 2 - no"))

        if answer==1:

 # Insert values into the table
            cursor.execute("INSERT INTO Payments (student_id, payment_date, number_of_classes, payment_method) VALUES (?, ?, ?, ?)",
               (student_id, date, number_of_classes, payment_type))
            conn.commit()

# View the Sessions table
            cursor.execute("SELECT * FROM Payments ORDER BY id DESC LIMIT 10")
            sessions = cursor.fetchall()

# Print the results
            print("\nPayments Table:")
            for session in sessions:
                print(session)

            insert_statement = f"INSERT INTO Payments (student_id, number_of_classes, payment_date, payment_method) VALUES ({student_id}, {date}, {number_of_classes}, {payment_type})"

        # Define the file name
            csv_file = 'inserted_data.csv'

# Open the file in write mode and save the inserted data
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)

    # Write the insert statement to the CSV file
                writer.writerow([insert_statement])
# Close the connection
            conn.close()
            break
        elif answer==2:
            continue
