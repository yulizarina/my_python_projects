
-- Create Students table to know needed information about students
CREATE TABLE Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50),
    subject_id INTEGER,
    city VARCHAR(50),
    country VARCHAR(50),
    enrollment_date DATE,
    graduation_date DATE,
    exam_date DATE,
    current_state VARCHAR(50),
    FOREIGN KEY (subject_id) REFERENCES Subjects(id)
);

-- Create Subjects table to see how many students attend each subject
CREATE TABLE Subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name VARCHAR(30)
);

-- Create Attendance table to track attended classes
CREATE TABLE Attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INT,
    date DATE,
    attended_that_day INT,
    balance_of_classes INT,
    FOREIGN KEY (student_id) REFERENCES Students(id)
);

-- Create Sessions table to track progress of each class
CREATE TABLE Sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INT,
    student_id INT,
    date DATE,
    payment VARCHAR(25),
    notes VARCHAR(255),
    FOREIGN KEY (subject_id) REFERENCES Subjects(id),
    FOREIGN KEY (student_id) REFERENCES Students(id)
);

-- Create Payments table
CREATE TABLE Payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INT,
    number_of_classes INT,
    payment_date DATE,
    payment_method VARCHAR(50),
    FOREIGN KEY (student_id) REFERENCES Students(id)
);

-- Create Indexes
CREATE INDEX idx_names_of_students ON Students (name);
CREATE INDEX idx_student_id_attendance ON Attendance (student_id);
CREATE INDEX idx_student_id_payments ON Payments (student_id);
CREATE INDEX idx_date_sessions ON Sessions (date);
CREATE INDEX idx_payment_date_payments ON Payments (payment_date);

-- Create Views
-- To see what students attend what classes
CREATE VIEW StudentSubjects AS
SELECT
    s.id AS student_id,
    s.first_and_last_name,
    subj.subject_id
FROM
    Students s
JOIN
    Subjects subj ON s.id = subj.student_id;

-- To track attendance of each student
CREATE VIEW StudentAttendance AS
SELECT
    s.id AS student_id,
    s.first_and_last_name AS name,
    a.status AS attendance_status,
    sess.date AS session_date,
    sess.notes AS session_notes
FROM
    Students s
JOIN
    Attendance a ON s.id = a.student_id
JOIN
    Sessions sess ON a.session_id = sess.id;

-- To track payments
CREATE VIEW StudentPayments AS
SELECT
    s.id AS student_id,
    s.first_and_last_name,
    p.id AS payment_id,
    p.number_of_classes,
    p.payment_date,
    p.payment_method
FROM
    Students s
JOIN
    Payments p ON s.id = p.student_id;
