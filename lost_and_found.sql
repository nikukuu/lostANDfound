-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 02, 2024 at 02:11 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lost_and_found`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_info`
--

CREATE TABLE `admin_info` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_info`
--

INSERT INTO `admin_info` (`id`, `username`, `password`) VALUES
(1, 'adminISUCC', 'scrypt:32768:8:1$1yJcPq3R2XStpDW6$d40c892aa527c2518ed78b6feb7a215c0c0235d5e0ea7d4e45dc2eeba0b218f2b4eb555e134e98357d1cfe62dfe24cb3a79dfa5f0202a71ec37b6b7d0af0b3c4');

-- --------------------------------------------------------

--
-- Table structure for table `claims`
--

CREATE TABLE `claims` (
  `id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `claimer_name` varchar(255) NOT NULL,
  `contact_info` varchar(255) DEFAULT NULL,
  `status` enum('pending','confirmed') DEFAULT 'pending',
  `message` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `claims`
--

INSERT INTO `claims` (`id`, `item_id`, `claimer_name`, `contact_info`, `status`, `message`) VALUES
(1, 6, 'Lalisa Manobal', '09123456789', 'confirmed', 'akin yang ballpen beh'),
(2, 3, 'Park G=Chaeyoung', 'chaeyoung@gmail.com', 'pending', 'yung tumbler ko beh akin yan beh pink pa yan dati pero ngayon black na'),
(3, 7, 'mharian angel', '09973177392', 'confirmed', 'aso ko yan beh Matcha pangalan');

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `id` int(11) NOT NULL,
  `item_name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `status` enum('pending','published','claimed') DEFAULT 'pending',
  `location` varchar(255) NOT NULL,
  `date_found` date NOT NULL,
  `image_path` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`id`, `item_name`, `description`, `status`, `location`, `date_found`, `image_path`) VALUES
(1, 'iphone', 'iphone X black', 'claimed', 'isu cauayan', '2024-11-24', 'static/uploads/isu-logo_new-green.png'),
(3, 'tumbler', 'black tumbler', 'published', 'isu cauayan', '2024-11-26', 'static/uploads/rylee.png'),
(4, 'umbrella', 'pink umbrella', 'published', 'isu cauayan', '2024-12-01', 'lily.jpg'),
(5, 'Eyeglasses', 'black eyeglass', 'published', 'IT building', '2024-12-01', 'dorm_sched.png'),
(6, 'ballpen', 'Gtech ballpen fuly paid', 'published', 'IT building', '2024-12-02', 'download.jpg'),
(7, 'dog', 'white, brown, black shitzu', 'claimed', 'sillawit cyn', '2024-12-02', 'IMG20240608061550.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_info`
--
ALTER TABLE `admin_info`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `claims`
--
ALTER TABLE `claims`
  ADD PRIMARY KEY (`id`),
  ADD KEY `item_id` (`item_id`);

--
-- Indexes for table `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin_info`
--
ALTER TABLE `admin_info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `claims`
--
ALTER TABLE `claims`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `items`
--
ALTER TABLE `items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `claims`
--
ALTER TABLE `claims`
  ADD CONSTRAINT `claims_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
