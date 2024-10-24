-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 31, 2024 at 06:07 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `user_management`
--

-- --------------------------------------------------------

--
-- Table structure for table `data_management`
--

CREATE TABLE `data_management` (
  `name` varchar(255) DEFAULT NULL,
  `id_number` varchar(255) DEFAULT NULL,
  `national_id` varchar(255) DEFAULT NULL,
  `area` varchar(255) DEFAULT NULL,
  `legal_action` varchar(255) DEFAULT NULL,
  `case_number` varchar(255) DEFAULT NULL,
  `payment_status` varchar(255) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `contract_issued` tinyint(1) DEFAULT NULL,
  `contract_date` date DEFAULT NULL,
  `files` varchar(255) DEFAULT NULL,
  `village` varchar(255) DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `file_status` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `data_management`
--

INSERT INTO `data_management` (`name`, `id_number`, `national_id`, `area`, `legal_action`, `case_number`, `payment_status`, `amount`, `payment_date`, `contract_issued`, `contract_date`, `files`, `village`, `reason`, `file_status`) VALUES
('احمد', '123', '30503211900675', '200', 'افراج', '1', 'تم', 23000.00, '2024-03-12', 0, '2024-03-12', 'C:/Users/CONNECT/OneDrive/Desktop/المستخلص السعودي/حصر شهر أغسطس.pdf', 'الرياح', 'مرفوض', 'مقبول');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `username` varchar(50) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`username`, `phone`, `email`, `password`) VALUES
('ahmed', '01029102507', 'ahmedibrahim01095773924@gmail.com', 'Ahmed@123');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
