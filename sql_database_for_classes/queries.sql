--Updating payment after each Session (one-time payment)
CREATE TRIGGER IF NOT EXISTS update_payment_for_one_timers_after_insert
AFTER INSERT ON Sessions
FOR EACH ROW
WHEN NEW.payment = 'one-time payment'
BEGIN
    INSERT INTO Payments (student_id, number_of_classes, payment_date, payment_method)
    VALUES (NEW.student_id, 1, NEW.date, 'r_card');
END;

CREATE TRIGGER IF NOT EXISTS update_payment_for_one_timers_after_update
AFTER UPDATE OF payment ON Sessions
FOR EACH ROW
WHEN NEW.payment = 'one-time payment'
BEGIN
    INSERT INTO Payments (student_id, number_of_classes, payment_date, payment_method)
    VALUES (NEW.student_id, 1, NEW.date, 'r_card');
END;

--Updating attendance for prepaid students after each session
CREATE TRIGGER IF NOT EXISTS update_balance_on_prepaid_after_session
AFTER INSERT ON Sessions
FOR EACH ROW
WHEN NEW.payment = 'prepaid'
BEGIN
   UPDATE Attendance
   SET balance_of_classes = balance_of_classes - 1,
       date = NEW.date
   WHERE student_id = NEW.student_id;
END;

--Updating attendance after a payment for prepaid
CREATE TRIGGER IF NOT EXISTS update_balance_from_payments
AFTER INSERT ON Payments
FOR EACH ROW
WHEN NEW.number_of_classes > 3
BEGIN
    -- Update the balance_of_classes if the student_id exists
    UPDATE Attendance
    SET balance_of_classes = balance_of_classes + NEW.number_of_classes,
        date = NEW.date
    WHERE student_id = NEW.student_id;

    -- If no rows were updated, insert a new record
    INSERT INTO Attendance (student_id, date, balance_of_classes)
    SELECT NEW.student_id, NEW.payment_date, NEW.number_of_classes
    WHERE (SELECT changes() = 0);
END;

CREATE VIEW active_students AS
SELECT Students.id, Students.name, Subjects.subject_name
FROM Students
JOIN Subjects ON Students.subject_id = Subjects.id
WHERE Students.current_state="enrolled";

CREATE VIEW payments_May AS
SELECT *
FROM payments
WHERE '2024-05-01' <= payment_date AND payment_date <= '2024-05-31';

--Fill out Subjects table
INSERT INTO Subjects (subject_name) VALUES ('SAT Math');
INSERT INTO Subjects (subject_name) VALUES ('College Math');
INSERT INTO Subjects (subject_name) VALUES ('Python');
INSERT INTO Subjects (subject_name) VALUES ('GRE Subject Test');
INSERT INTO Subjects (subject_name) VALUES ('EGE Profil');
INSERT INTO Subjects (subject_name) VALUES ('GRE General');
INSERT INTO Subjects (subject_name) VALUES ('GMAT');

SELECT *
FROM subjects;

-- Fill out students table

INSERT INTO students (name, subject_id, city, country, enrollment_date,  graduation_date, exam_date, current_state)
VALUES ('Jonathan', 1, 'Moscow','Russia','2023-11-30', NULL, '2024-08-24', 'enrolled');
INSERT INTO students (name, subject_id, city, country, enrollment_date,  graduation_date, exam_date, current_state)
VALUES ('Anna', 1, NULL, 'Moldova', '2024-02-08', NULL, '2024-08-24', 'enrolled');
INSERT INTO students (name, subject_id, city, country, enrollment_date,  graduation_date, exam_date, current_state)
VALUES ('Maria', 2, NULL, 'Turkey', '2023-10-15', NULL, NULL, 'enrolled');
INSERT INTO students (name, subject_id, city, country, enrollment_date,  graduation_date, exam_date, current_state)
VALUES ('Darina', 1, 'Crimea', 'Russia', '2026-03-11', NULL, NULL, 'enrolled');
INSERT INTO students (name, subject_id, city, country, enrollment_date,  graduation_date, exam_date, current_state)
VALUES ('Darina VSE', 3, 'Moscow','Russia', '2024-05-28', NULL, '2024-06-11', 'enrolled');
INSERT INTO students (name, subject_id, city, country, enrollment_date,  graduation_date, exam_date, current_state)
VALUES ('Patricija', 1, 'Toronto', 'Canada', '2024-05-28', NULL, '2024-06-11', 'enrolled');
INSERT INTO students (name, subject_id, city, country, enrollment_date,  graduation_date, exam_date, current_state)
VALUES ('Galina', 4, 'Moscow','Russia', '2024-05-18', NULL, '2024-09-15', 'enrolled');
INSERT INTO students (name, subject_id, city, country, enrollment_date,  graduation_date, exam_date, current_state)
VALUES ('Yaroslav', 5, 'Moscow','Russia', '2024-05-18', NULL, '2024-09-15', 'graduated');
INSERT INTO students (name, subject_id, city, country, enrollment_date,  graduation_date, exam_date, current_state)
VALUES ('Anastasia', 1, 'Miami','USA', '2018-05-18', NULL, '2024-08-24', 'enrolled');
INSERT INTO students (name, subject_id, city, country, enrollment_date,  graduation_date, exam_date, current_state)
VALUES ('Ksenia', 5, 'Moscow','Russia', '2024-03-10', NULL, '2024-06-01', 'enrolled');
INSERT INTO students (name, subject_id, city, country, enrollment_date,  graduation_date, exam_date, current_state)
VALUES ('one-timer SAT', 1, NULL, NULL, NULL, NULL, NULL, 'enrolled');
INSERT INTO students (name, subject_id, city, country, enrollment_date,  graduation_date, exam_date, current_state)
VALUES ('one-timer Cmath', 2, NULL, NULL, NULL, NULL, NULL, 'enrolled');
INSERT INTO students (name, subject_id, city, country, enrollment_date,  graduation_date, exam_date, current_state)
VALUES ('one-timer Python', 3, NULL, NULL, NULL, NULL, NULL, 'enrolled');
INSERT INTO students (name, subject_id, city, country, enrollment_date,  graduation_date, exam_date, current_state)
VALUES ('one-timer gre st', 4, NULL, NULL, NULL, NULL, NULL, 'enrolled');
INSERT INTO students (name, subject_id, city, country, enrollment_date,  graduation_date, exam_date, current_state)
VALUES ('one-timer ege', 5, NULL, NULL, NULL, NULL, NULL, 'enrolled');
INSERT INTO students (name, subject_id, city, country, enrollment_date,  graduation_date, exam_date, current_state)
VALUES ('Alina', 1, 'Tashkent', 'Uzbekistan', '2024-06-18', NULL, '2024-08-24', 'enrolled');
INSERT INTO students (name, subject_id, city, country, enrollment_date,  graduation_date, exam_date, current_state)
VALUES ('Yulia', 1, 'Moscow', 'Russia', '2024-06-26', NULL, '2024-08-24', 'enrolled');

--Updating graduated students
UPDATE students
SET graduation_date = 'graduated', exam_date = '2024-06-01'
WHERE name='Yaroslav';

UPDATE students
SET current_state = '2024-06-01', graduation_date = '2024-05-30'
WHERE name='Ksenia';

--Sessions before May 20th


--Enter the balance of classes as of May 20th
INSERT INTO Attendance ( student_id, date, balance_of_classes) VALUES (2,'2024-05-20',31); --Anna
INSERT INTO Attendance ( student_id, date, balance_of_classes) VALUES (6,'2024-05-20',6); --Patricija
INSERT INTO Attendance ( student_id, date, balance_of_classes) VALUES (1,'2024-05-20',5); --John
INSERT INTO Attendance ( student_id, date, balance_of_classes) VALUES (9,'2024-05-20',2); --Anastasia Miami

--Payment Galina 8
INSERT INTO Payments (student_id, number_of_classes, payment_date, payment_method) VALUES (7,8, '2024-06-17', 'r_card');

-- Create Sessions table to track progress of each class
-- Tuesday, May, 21
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 2, '2024-05-21','prepaid', 'exam prep');

-- Wednesday, May, 22
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (4,7,'2024-05-22','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 1, '2024-05-22','prepaid', 'exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 1, '2024-05-22','prepaid', 'exam prep');

-- Tuesday, May, 23
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 2, '2024-05-23','prepaid', 'exam prep');

-- Friday, May, 24
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 1, '2024-05-24','prepaid', 'exam prep');

-- Saturday May, 25
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 1, '2024-05-25','prepaid', 'exam prep');

-- Wednesday, May, 26
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (4,7,'2024-05-26','prepaid','exam prep');

-- Tuesday, May, 27
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 2, '2024-05-27','prepaid', 'exam prep');

-- Tuesday May, 28
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 2, '2024-05-28', 'prepaid','geometry' );

-- Wednesday May, 29
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (3, 5,'2024-05-29', 'one-time payment','loops and lists');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 2, '2024-05-29', 'prepaid','geometry' );

-- Thursday May, 30
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (5,8, '2024-05-31', 'one-time payment', 'final prep for the exam' );
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (2,3, '2024-05-31', 'one-time payment', 'prep for the exam' );
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (5,10, '2024-05-31', 'one-time payment', 'prep for the exam' );

-- Friday May, 31
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,1, '2024-05-31', 'prepaid', 'no show' );
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,2, '2024-05-31', 'prepaid', 'triangles' );

-- Saturday June, 1
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (3, 5,'2024-06-01','one-time payment', 'more on dictionaries');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 1, '2024-06-01','prepaid', 'geometry');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 9, '2024-06-01', 'prepaid','sort sat students bank');

-- Sunday June, 2
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,6,'2024-06-02','prepaid','equivalent expressions, need more of these');

-- Sunday June, 3
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (3,13,'2024-06-02','one-time payment','exam prep');

-- Thursday June, 5 Jhon, Darina, sat-onetimer
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,1,'2024-06-05','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,11,'2024-06-05','one-time payment','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (3,13,'2024-06-05','one-time payment','exam prep');

-- Friday June, 7 - John, python one-timer
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,1,'2024-06-07','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (3,13,'2024-06-07','one-time payment','exam prep');

-- Saturday June, 8 - python one-timer
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (3,13,'2024-06-08','one-time payment','exam prep');

-- Sunday June, 9 - Patricija
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,6,'2024-06-09','prepaid','exam prep');

-- Monday June, 10 - python one-timer
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (3,13,'2024-06-10','one-time payment','exam prep');


-- Tuesday June, 11 - python one-timer
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (3,13,'2024-06-11','one-time payment','exam prep');

-- Wednesday June, 12 John Галина Дарина П
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (3,13,'2024-06-12','one-time payment','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,1,'2024-06-12','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (4,7,'2024-06-12','prepaid','exam prep');

-- Thursday June, 13 Дарина П
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (3,13,'2024-06-13','one-time payment','exam prep');

-- Friday June, 14 John
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,1,'2024-06-14','prepaid','exam prep');

-- Saturday June, 15 anastasia, john, onetimersat
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,9,'2024-06-15','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,1,'2024-06-15','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,11,'2024-06-15','one-time payment','exam prep');

--Payment Anastasia
INSERT INTO Payments (student_id, number_of_classes, payment_date, payment_method) VALUES (9,8, '2024-06-17', 'moneygram');

-- Monday June, 17 patricia, one-timer collegemath
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (2,12,'2024-06-17','one-time payment','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,6,'2024-06-17','prepaid','exam prep');

--Payment John 20
INSERT INTO Payments (student_id, number_of_classes, payment_date, payment_method) VALUES (1,20, '2024-06-17', 'r_card');

-- Tuesday June, 18 anastasia, patricia
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 16, '2024-06-18', 'one-time payment', 'equivalent expressions');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,9,'2024-06-18','prepaid','exam prep');

-- Wednesday June, 19 one-timer colmath, galina
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (2,12,'2024-06-19','one-time payment','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (4,7,'2024-06-19','prepaid','exam prep');

-- Thursday June, 20 anastasia, alina
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,9,'2024-06-20','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 16, '2024-06-20', 'one-time payment', 'convert, isolate a variable');

-- Friday June, 21 john, onetimer collegemath
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (2,12,'2024-06-21','one-time payment','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,1,'2024-06-21','prepaid','exam prep');

-- Monday June, 24 Anna, john
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,1,'2024-06-24','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,2,'2024-06-24','prepaid','exam prep');

-- Tuesday June, 25 onetimer collegemath, john, anna, alina
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (2,12,'2024-06-25','one-time payment','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 16, '2024-06-25', 'one-time payment', 'linear function');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,1,'2024-06-25','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,2,'2024-06-25','prepaid','exam prep');

-- Wednesday June, 26
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,2,'2024-06-26','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,17,'2024-06-26','one-time payment','exam prep');

-- Thursday June, 27 john, galina, anastasia, anna, alina
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,9,'2024-06-27','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,1,'2024-06-27','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,2,'2024-06-27','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (4,7,'2024-06-27','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,16,'2024-06-27','one-time payment','linear funct word problem');

-- Friday June, 28 anna
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,2,'2024-06-27','prepaid','exam prep');

-- Payments Yulia
INSERT INTO Payments (student_id, number_of_classes, payment_date, payment_method) VALUES (17,8, '2024-06-29', 'r_card');

-- Sunday June, 30 galina, yulia
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,17,'2024-06-30','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (4,7,'2024-06-30','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,9,'2024-06-30','prepaid','exam prep');

-- Monday July, 1 john,
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,1,'2024-07-01','prepaid','exam prep');

-- Tuesday July, 2 john, yulia, anna, alina
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,1,'2024-07-02','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,2,'2024-07-02','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 16, '2024-07-02','one-time payment','quadratic function and equations');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,17,'2024-07-02','prepaid','exam prep');

-- Wednesday July, 3 john anna
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,1,'2024-07-03','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,2,'2024-07-03','prepaid','exam prep');

-- Thursday July, 4 yulia, patricija, anastasia, alina, galina
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,6,'2024-07-04','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 9, '2024-07-04', 'prepaid', 'question bank');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1,17,'2024-07-02','prepaid','exam prep');
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (4,7,'2024-07-04','prepaid','exam prep');

-- Friday July, 5
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 9, '2024-07-05', 'prepaid', 'question bank');

-- Sunday July, 7
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 17, 2024-07-07, prepaid, scatterplot+quadratic f);
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 9, 2024-07-07, prepaid, question bank);
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (4, 7, 2024-07-07, prepaid, diff equations);

-- Monday July, 8
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 2, 2024-07-08, prepaid, inequalities);
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 1, 2024-07-08, prepaid, geometry);

-- Tuesday July, 9
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 2, 2024-07-09, prepaid, prep)
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 9, 2024-07-09, prepaid, prep)
INSERT INTO Sessions (subject_id, student_id, date, payment, notes) VALUES (1, 17, 2024-07-09, prepaid, prep)

-- Wednesday July, 10

-- Friday July, 12

SELECT *
FROM students;

--Sessions

