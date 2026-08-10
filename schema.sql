-- schema.sql - Complete MySQL Script for XAMPP phpMyAdmin with 8-Subject Daily Timetable (40 Periods)
CREATE DATABASE IF NOT EXISTS `student_db`;
USE `student_db`;

-- 1. USERS TABLE
CREATE TABLE IF NOT EXISTS `users` (
  `id` VARCHAR(50) PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL,
  `role` VARCHAR(20) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `subject` VARCHAR(100) DEFAULT NULL,
  `class` VARCHAR(50) DEFAULT NULL,
  `phone` VARCHAR(50) DEFAULT NULL,
  `child_id` VARCHAR(50) DEFAULT NULL
);

-- 2. STUDENTS TABLE
CREATE TABLE IF NOT EXISTS `students` (
  `id` VARCHAR(50) PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL,
  `student_id` VARCHAR(50) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `class` VARCHAR(50) NOT NULL,
  `attendance` INT DEFAULT 90,
  `parent_name` VARCHAR(100) DEFAULT NULL,
  `teacher_remarks` TEXT DEFAULT NULL
);

-- 3. MARKS TABLE
CREATE TABLE IF NOT EXISTS `marks` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `student_id` VARCHAR(50) NOT NULL,
  `physics` INT DEFAULT 75,
  `maths` INT DEFAULT 75,
  `chemistry` INT DEFAULT 75,
  `computer_science` INT DEFAULT 75,
  `english` INT DEFAULT 85,
  `biology` INT DEFAULT 72,
  `env_science` INT DEFAULT 88,
  `physical_edu` INT DEFAULT 95,
  FOREIGN KEY (`student_id`) REFERENCES `students`(`id`) ON DELETE CASCADE
);

-- 4. TIMETABLE TABLE (8 Subjects Daily)
CREATE TABLE IF NOT EXISTS `timetable` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `period` INT NOT NULL,
  `day` VARCHAR(20) NOT NULL,
  `time` VARCHAR(50) NOT NULL,
  `subject` VARCHAR(100) NOT NULL,
  `teacher` VARCHAR(100) NOT NULL,
  `room` VARCHAR(50) NOT NULL
);

-- 5. QUIZZES TABLE
CREATE TABLE IF NOT EXISTS `quizzes` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(100) NOT NULL,
  `subject` VARCHAR(50) DEFAULT 'Physics',
  `score` INT DEFAULT 75,
  `total` INT DEFAULT 100,
  `date` DATE NOT NULL
);

-- Inserters
INSERT INTO `users` (`id`, `name`, `role`, `email`, `password`, `subject`, `class`, `phone`, `child_id`) VALUES
('u1', 'Dr. Sarah Vance', 'ADMINISTRATOR', 'admin@school.com', 'admin123', NULL, NULL, NULL, NULL),
('u2', 'Prof. Marcus Sterling', 'TEACHER', 'teacher@school.com', 'teacher123', 'Physics & Math', 'Class 10-A', NULL, NULL),
('u3', 'Alex Rivera', 'STUDENT', 'alex@student.com', 'student123', NULL, 'Class 10-A', NULL, NULL),
('u4', 'Sophia Chen', 'STUDENT', 'sophia@student.com', 'student123', NULL, 'Class 10-A', NULL, NULL),
('u5', 'Robert Rivera', 'PARENT', 'robert@parent.com', 'parent123', NULL, NULL, '+1 555-0192', 'u3')
ON DUPLICATE KEY UPDATE `name`=`name`;

INSERT INTO `students` (`id`, `name`, `student_id`, `password`, `class`, `attendance`, `parent_name`, `teacher_remarks`) VALUES
('u3', 'Alex Rivera', 'STU-101', 'student123', 'Class 10-A', 72, 'Robert Rivera', 'Alex is doing great in Computer Science, but needs extra practice in Physics.'),
('u4', 'Sophia Chen', 'STU-102', 'student123', 'Class 10-A', 98, 'Jennifer Chen', 'Outstanding academic performance and class leadership.')
ON DUPLICATE KEY UPDATE `name`=`name`;

-- Insert 8 Subjects Daily Timetable
DELETE FROM `timetable`;
INSERT INTO `timetable` (`period`, `day`, `time`, `subject`, `teacher`, `room`) VALUES
(1, 'Monday', '08:30 AM - 09:15 AM', 'Physics', 'kamal mam', 'Lab 1'),
(2, 'Monday', '09:15 AM - 10:00 AM', 'Maths', 'sunita mam', 'Room 204'),
(3, 'Monday', '10:00 AM - 10:45 AM', 'Chemistry', 'geenu mam', 'Lab 2'),
(4, 'Monday', '10:45 AM - 11:30 AM', 'Computer Science', 'Ashita mam', 'CompLab A'),
(5, 'Monday', '11:30 AM - 12:15 PM', 'Physics Lab', 'ankur sir', 'Lab 1'),
(6, 'Monday', '01:00 PM - 01:45 PM', 'English Literature', 'Priya mam', 'Room 101'),
(7, 'Monday', '01:45 PM - 02:30 PM', 'Biology', 'Ravi sir', 'BioLab'),
(8, 'Monday', '02:30 PM - 03:15 PM', 'Physical Education', 'Vikram sir', 'Sports Ground'),

(1, 'Tuesday', '08:30 AM - 09:15 AM', 'Maths', 'sunita mam', 'Room 204'),
(2, 'Tuesday', '09:15 AM - 10:00 AM', 'Physics', 'kamal mam', 'Lab 1'),
(3, 'Tuesday', '10:00 AM - 10:45 AM', 'Computer Science', 'Ashita mam', 'CompLab A'),
(4, 'Tuesday', '10:45 AM - 11:30 AM', 'Chemistry', 'geenu mam', 'Lab 2'),
(5, 'Tuesday', '11:30 AM - 12:15 PM', 'Physics Lab', 'ankur sir', 'Lab 1'),
(6, 'Tuesday', '01:00 PM - 01:45 PM', 'English Literature', 'Priya mam', 'Room 101'),
(7, 'Tuesday', '01:45 PM - 02:30 PM', 'Biology', 'Ravi sir', 'BioLab'),
(8, 'Tuesday', '02:30 PM - 03:15 PM', 'Physical Education', 'Vikram sir', 'Sports Ground'),

(1, 'Wednesday', '08:30 AM - 09:15 AM', 'Chemistry', 'geenu mam', 'Lab 2'),
(2, 'Wednesday', '09:15 AM - 10:00 AM', 'Computer Science', 'Ashita mam', 'CompLab A'),
(3, 'Wednesday', '10:00 AM - 10:45 AM', 'Physics Lab', 'ankur sir', 'Lab 1'),
(4, 'Wednesday', '10:45 AM - 11:30 AM', 'Maths', 'sunita mam', 'Room 204'),
(5, 'Wednesday', '11:30 AM - 12:15 PM', 'Physics', 'kamal mam', 'Lab 1'),
(6, 'Wednesday', '01:00 PM - 01:45 PM', 'English Literature', 'Priya mam', 'Room 101'),
(7, 'Wednesday', '01:45 PM - 02:30 PM', 'Biology', 'Ravi sir', 'BioLab'),
(8, 'Wednesday', '02:30 PM - 03:15 PM', 'Physical Education', 'Vikram sir', 'Sports Ground'),

(1, 'Thursday', '08:30 AM - 09:15 AM', 'Computer Science', 'Ashita mam', 'CompLab A'),
(2, 'Thursday', '09:15 AM - 10:00 AM', 'English Literature', 'Priya mam', 'Room 101'),
(3, 'Thursday', '10:00 AM - 10:45 AM', 'Maths', 'sunita mam', 'Room 204'),
(4, 'Thursday', '10:45 AM - 11:30 AM', 'Physics', 'kamal mam', 'Lab 1'),
(5, 'Thursday', '11:30 AM - 12:15 PM', 'Physics Lab', 'ankur sir', 'Lab 1'),
(6, 'Thursday', '01:00 PM - 01:45 PM', 'Chemistry', 'geenu mam', 'Lab 2'),
(7, 'Thursday', '01:45 PM - 02:30 PM', 'Biology', 'Ravi sir', 'BioLab'),
(8, 'Thursday', '02:30 PM - 03:15 PM', 'Physical Education', 'Vikram sir', 'Gym'),

(1, 'Friday', '08:30 AM - 09:15 AM', 'Physics', 'kamal mam', 'Lab 1'),
(2, 'Friday', '09:15 AM - 10:00 AM', 'Maths', 'sunita mam', 'Room 204'),
(3, 'Friday', '10:00 AM - 10:45 AM', 'Chemistry', 'geenu mam', 'Lab 2'),
(4, 'Friday', '10:45 AM - 11:30 AM', 'Computer Science', 'Ashita mam', 'CompLab A'),
(5, 'Friday', '11:30 AM - 12:15 PM', 'Physics Lab', 'ankur sir', 'Lab 1'),
(6, 'Friday', '01:00 PM - 01:45 PM', 'English Literature', 'Priya mam', 'Room 101'),
(7, 'Friday', '01:45 PM - 02:30 PM', 'Biology', 'Ravi sir', 'BioLab'),
(8, 'Friday', '02:30 PM - 03:15 PM', 'Physical Education', 'Vikram sir', 'Sports Ground');
