
-- Create Students table to know needed information about students
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Subjects;
DROP TABLE IF EXISTS Attendance;
DROP TABLE IF EXISTS Sessions;
DROP TABLE IF EXISTS Payments;

DROP INDEX IF EXISTS idx_names_of_students;
DROP INDEX IF EXISTS idx_student_id_attendance;
DROP INDEX IF EXISTS idx_student_id_payments;
DROP INDEX IF EXISTS idx_date_sessions;
DROP INDEX IF EXISTS idx_payment_date_payments;

-- Create Views

DROP VIEW IF EXISTS StudentSubjects;
DROP VIEW IF EXISTS StudentAttendance;
DROP VIEW IF EXISTS StudentPayments;
DROP VIEW IF EXISTS active_students;
DROP VIEW IF EXISTS payments_May;

DROP TRIGGER IF EXISTS update_payment_for_one_timers_after_insert;
DROP TRIGGER IF EXISTS update_payment_for_one_timers_after_update;
DROP TRIGGER IF EXISTS update_balance_on_prepaid_after_session;
DROP TRIGGER IF EXISTS update_balance_fom_payments;
