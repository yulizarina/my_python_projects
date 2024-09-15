import sqlite3
from datetime import datetime, timedelta
import csv

# Connect to the SQLite database
conn = sqlite3.connect('my_classes.db')
cursor = conn.cursor()

# Get the current date
date = datetime.now().date()

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
        date = str(datetime.now().date() - timedelta(days=0))
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
        payment = 'one-time payment'
    else:
        payment=int(input("Type of payment? Enter 1 : prepaid, 2 : one-time payment "))
        if payment == int(1):
            payment = 'prepaid'
        elif payment == int(2):
            payment = 'one-time payment'

    notes = input("Enter any notes: ")
    answer=int(input(f"""Looks good?
                     subject_id:{subject_id}
                     student_id: {student_id}
                     date:{date}
                     payment:{payment}
                     notes:{notes}
                     Enter 1 - yes, 2 - no  """))
    if answer==int(1):
        insert_statement = f"INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES ({subject_id}, {student_id}, {date}, {payment}, {notes})"
 # Insert values into the table
        cursor.execute("INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (?, ?, ?, ?, ?)",
               (subject_id, student_id, date, payment, notes))
        conn.commit()

# View the Sessions table
        cursor.execute("SELECT * FROM Sessions")
        sessions = cursor.fetchall()

# Print the results
        print("\nSessions Table:")
        for session in sessions:
            print(session)

        # View the Attendance table
        attendance_table=[]
        cursor.execute("SELECT students.name, attendance.balance_of_classes, attendance.date FROM Students JOIN Attendance ON attendance.student_id = students.id;")
        sessions = cursor.fetchall()

# Print the results
        b = 0
        print("\nAttendance Table:")
        for session in sessions:
            print(session)
            if str(session[1])=='1' or str(session[1])=='0':
                b = b + 1
                print("!!!   Classes report for ",session[0])
                cursor.execute(f"SELECT number_of_classes, payment_date FROM Payments WHERE student_id=(SELECT id FROM Students WHERE name='{session[0]}')")
                payment_records = cursor.fetchall()
                cursor.execute(f"SELECT date, notes FROM Sessions WHERE student_id=(SELECT id FROM Students WHERE name='{session[0]}')")
                attendance_dates = cursor.fetchall()

                if payment_records:
                    last_paid_classes, last_paid_date = payment_records[0] #list of tuples where I get the number of classes
                    last_paid_classes=int(last_paid_classes)
                    attendance_dates = attendance_dates[-last_paid_classes:]

                with open(f'class_dates{b}.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["date"])  # Write the header
                    for date in attendance_dates:
                        writer.writerow([date[0]])

                print("Dates written to class_dates.csv")

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
    elif answer==int(2):
        continue

