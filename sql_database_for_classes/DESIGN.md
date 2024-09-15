# Design Document

By IULIIA ZADORINA

Video overview: <(https://youtu.be/5hoA0QjhkW0)>

## Scope

In this section you should answer the following questions:

* The purpose of the database is to keep track of classes attended and payments made to automate reports generation
* In my database I include my students, the subjects that I teach, the number of attended classes, the number of paid classes.
* Students that are no longer taking classes, the amount students pay, students'age would be outside of the scope of my database.

## Functional Requirements

In this section you should answer the following questions:

* User will be able to view the number of remaining classes for any student, when the classes occure, what subject brinngs most classes, total number of classes in a certain time period (a week, a month)
* Users' personal data, total income, at what time the classes were taken are beyond the scope of what a user should be able to do with my database.

## Representation

![Entity relationship diagram](entity_diagram.png)


### Entities

1. Entities:

Students
Subjects
Sessions
Attendance
Payments

2. Attributes:

Students:

id (Primary Key, Integer, Auto Increment)
first_name (String, up to 50 characters)
last_name (String, up to 50 characters)
enrollment_date (Date)
graduation_date (Date)
exam_date (Date)
current_state (String, e.g., active, graduated, etc.)

Subjects:

subjects_id (Primary Key, Integer, Auto Increment)
student_id (Int, Foreign key)

Attendance:

id (Primary Key, Integer, Auto Increment)
student_id (Foreign Key to Students, Integer)
number_of_classes (Foreign Key to Payments, Integer)
balance_of_classes (Integer)

Sessions:

id (Primary Key, Integer, Auto Increment)
subject_id (Foreign Key to Subjects, Integer)
student_id (Foreign Key to Students, Integer)
date (Date)
status (String, e.g., on time, late, absent)
notes (String)

Payments:

id (Primary Key, Integer, Auto Increment)
student_id (Foreign Key to Students, Integer)
number_of_classes (Integer)
payment_date (Date)
payment_method (String, e.g., credit card, PayPal, etc.)

3. Reasoning for the chosen types:
Integer: Used for IDs because they are efficient and suitable for auto-incremented primary keys.
String: Used for names, descriptions, and statuses because they need to store text data of varying lengths.
Date: Used for dates (e.g., birth, enrollment, session dates) to ensure proper date formatting and enable date-specific queries.
Time: Used for start and end times of class sessions to capture precise timing.

4. Reasoning for the constraints:
Primary Key: Ensures each record is uniquely identifiable, maintaining data integrity and enabling efficient retrieval.
Foreign Key: Establishes relationships between tables (e.g., linking students to attendance records, courses to sessions), enforcing referential integrity.
Unique: Ensures attributes like email are not duplicated, preventing conflicts.
Not Null: Applied to essential attributes (e.g., first_name, last_name, email) to ensure critical data is always provided.
Default Values: Used for attributes like status in Students (e.g., default to 'active') to maintain a default state for new records.

### Relationships

Students and Subjects: One student can enroll in many subjects. This is a one-to-many relationship, as each student can have multiple subject records in the Subjects table.
Students and Attendance: One student can have many attendance records. This is also a one-to-many relationship, as each student can have multiple attendance records in the Attendance table.
Subjects and Sessions: One subject can have many sessions. This is a one-to-many relationship, as each subject can have multiple session records in the Sessions table.
Students and Sessions: One student can attend many sessions, and one session can have many students. This is a many-to-many relationship.
Students and Payments: One student can make many payments. This is a one-to-many relationship, as each student can have multiple payment records in the Payments table.

Description:

Students table stores information about students, including their names, enrollment and graduation dates, exam dates, and status.
Subjects table links students to the subjects they are enrolled in.
Attendance table tracks student attendance for each session, showing whether the student was present or absent.
Sessions table contains information about each session, such as the subject, date, and any notes.
Payments table records payments made by students, including the number of classes covered, payment date, and payment method.

## Optimizations

Indexes: Indexes help speed up searches in the database. They were added to columns like student_id and date in the Sessions table, student_id in the Attendance table, and student_id in the Payments table. This makes it faster to find specific information in these tables.

Views: Views make it easier to read and write complex queries. For instance, a view could combine information from the Students and Subjects tables to show which subjects each student is studying. This means you don't have to write long queries every time you need this information.

## Limitations

Limited Scalability: The design could have trouble handling more students, subjects, sessions, and payments. While indexes help, a lot of data might slow down queries.

Complex Queries: The database might struggle with really complicated queries that involve lots of joins and calculations. This could make the database slower.

What the database might not do well:

Limited Historical Data: The design doesn't track changes to student enrollment or keep a history of attendance.

Limited Reporting Capabilities: The database can store basic information about students, subjects, attendance, sessions, and payments, but it might need extra work or tools for more advanced reporting.
