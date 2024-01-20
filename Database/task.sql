-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 19, 2024 at 05:52 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `taskmanager`
--

-- --------------------------------------------------------

--
-- Table structure for table `task`
--

CREATE TABLE `task` (
  `task_id` varchar(20) NOT NULL,
  `task_name` varchar(90) NOT NULL,
  `task_description` varchar(96) NOT NULL,
  `task_created_time` datetime NOT NULL DEFAULT current_timestamp(),
  `task_created_by` varchar(20) NOT NULL,
  `task_due_by` date NOT NULL,
  `task_status` varchar(20) NOT NULL,
  `task_priority` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='task table';

--
-- Dumping data for table `task`
--

INSERT INTO `task` (`task_id`, `task_name`, `task_description`, `task_created_time`, `task_created_by`, `task_due_by`, `task_status`, `task_priority`) VALUES
('TASK-01', 'zoom meeeting with shareholder', 'prepare for shareholder F&Q', '2024-01-18 12:31:33', 'admin', '2024-01-29', 'In Progress', 'High'),
('TASK-02', 'general meeting', 'with all the stakeholder', '2024-01-18 16:14:42', 'admin', '2024-01-08', 'Completed', 'Normal'),
('TASK-03', 'decoration for annual meeting ', 'prepare for decoration', '2024-01-19 12:06:00', 'admin', '2024-01-31', 'Not Started', 'High'),
('TASK-04', 'Coffee machine purchase', 'buy a coffee machine for pantry', '2024-01-19 12:15:14', 'admin', '2024-02-29', 'In Progress', 'Low'),
('TASK-05', 'Company Gathering', 'Gathering at the Singapore River', '2024-01-19 12:22:59', 'Saerah ', '2024-02-11', 'Not Started', 'High'),
('TASK-06', 'Office Discussion ', 'Discussion by each department head', '2024-01-19 12:24:52', 'Saerah ', '2024-01-19', 'Not Started', 'Urgent');

--
-- Triggers `task`
--
DELIMITER $$
CREATE TRIGGER `task_id_increment` BEFORE INSERT ON `task` FOR EACH ROW BEGIN
    DECLARE next_id INT;
    SELECT (SUBSTRING(MAX(task_id), 3) + 1) INTO next_id FROM task;
    
    IF next_id IS NULL THEN
        SET next_id = 1;
    END IF;

    WHILE (SELECT COUNT(*) FROM task WHERE task_id = CONCAT('TASK-', LPAD(next_id, 2, '0'))) > 0 DO
        SET next_id = next_id + 1;
    END WHILE;
    
    SET NEW.task_id = CONCAT('TASK-', LPAD(next_id, 2, '0'));
END
$$
DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
