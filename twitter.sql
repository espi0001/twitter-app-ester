-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mariadb
-- Generation Time: Oct 22, 2025 at 09:51 AM
-- Server version: 10.6.20-MariaDB-ubu2004
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `twitter`
--

-- --------------------------------------------------------

--
-- Table structure for table `people`
--

CREATE TABLE `people` (
  `person_pk` bigint(20) UNSIGNED NOT NULL,
  `person_first_name` varchar(20) NOT NULL,
  `person_last_name` varchar(20) NOT NULL,
  `person_age` tinyint(3) UNSIGNED NOT NULL,
  `person_nickname` varchar(20) NOT NULL,
  `person_cpr_number` char(10) NOT NULL,
  `person_phone_number` varchar(17) NOT NULL,
  `item_price` decimal(5,2) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `people`
--

INSERT INTO `people` (`person_pk`, `person_first_name`, `person_last_name`, `person_age`, `person_nickname`, `person_cpr_number`, `person_phone_number`, `item_price`) VALUES
(1, 'Sara ', 'Meisner', 26, 'Zaza', '2904991234', '42706454', 123.95),
(2, 'Carl', 'Andrews', 25, 'Carlitos', '1007001234', '22222222', 123.00);

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `post_pk` bigint(20) UNSIGNED NOT NULL,
  `user_fk` bigint(20) UNSIGNED NOT NULL,
  `post_message` varchar(280) NOT NULL,
  `post_total_likes` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`post_pk`, `user_fk`, `post_message`, `post_total_likes`) VALUES
(1, 1, 'one', 10),
(2, 1, 'two', 20),
(3, 1, 'three', 30),
(4, 8, 'four', 40),
(5, 8, 'five', 50),
(6, 1, 'six', 60),
(7, 9, 'seven', 70);

-- --------------------------------------------------------

--
-- Table structure for table `trending`
--

CREATE TABLE `trending` (
  `trend_pk` bigint(20) UNSIGNED NOT NULL,
  `trend_title` varchar(100) NOT NULL,
  `trend_message` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `trending`
--

INSERT INTO `trending` (`trend_pk`, `trend_title`, `trend_message`) VALUES
(1, 'one', 'trend one'),
(2, 'two', 'trend two'),
(3, 'three', 'trend three'),
(4, 'four', 'trend four'),
(5, 'five', 'trend five');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_pk` bigint(20) UNSIGNED NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `user_password` varchar(255) NOT NULL,
  `user_username` varchar(20) NOT NULL,
  `user_first_name` varchar(20) NOT NULL,
  `user_last_name` varchar(20) NOT NULL,
  `user_avatar_path` varchar(50) DEFAULT NULL,
  `verification_key` char(42) DEFAULT NULL,
  `user_activated_at` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_pk`, `user_email`, `user_password`, `user_username`, `user_first_name`, `user_last_name`, `user_avatar_path`, `verification_key`, `user_activated_at`) VALUES
(1, 'a@a.com', 'scrypt:32768:8:1$8Tk2zopyEtkmgUbk$7341cf48a9b7a9f1f5dade2c3565f81450d5ce98a675e3cefd20f07aff9cfbcebabf403b9e1bc010d35d43d486e7ae395ef9e80640fd7e73687be51a5f2f2df0', 'sarameisner', 'Sara', 'Meisner', 'https://avatar.iran.liara.run/public/40', '', 0),
(8, 'a@b.com', 'scrypt:32768:8:1$8Tk2zopyEtkmgUbk$7341cf48a9b7a9f1f5dade2c3565f81450d5ce98a675e3cefd20f07aff9cfbcebabf403b9e1bc010d35d43d486e7ae395ef9e80640fd7e73687be51a5f2f2df0', 'ester', 'Ester', 'Piazza', 'https://avatar.iran.liara.run/public/70', '', 0),
(9, 'a@c.com', 'scrypt:32768:8:1$8Tk2zopyEtkmgUbk$7341cf48a9b7a9f1f5dade2c3565f81450d5ce98a675e3cefd20f07aff9cfbcebabf403b9e1bc010d35d43d486e7ae395ef9e80640fd7e73687be51a5f2f2df0', 'ccarl', 'Carl', 'Andrews', 'https://avatar.iran.liara.run/public/54', '', 0),
(31, 'espi0001@gmail.com', 'scrypt:32768:8:1$K1IMIcm6nrvk3y5D$1f3277b8f2e315e9d64a9bba3a2f41cf2431cb80cd1b0920f84720e9a8ce29895e9efe1183ab29c1750ad05c346700067a13c1f99e91eb771aed9a65e9b52632', 'espi', 'ester', 'piazza', NULL, NULL, 1761126385);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `people`
--
ALTER TABLE `people`
  ADD UNIQUE KEY `person_pk` (`person_pk`),
  ADD UNIQUE KEY `person_cpr_number` (`person_cpr_number`),
  ADD UNIQUE KEY `person_phone_number` (`person_phone_number`),
  ADD KEY `person_first_name` (`person_first_name`),
  ADD KEY `person_last_name` (`person_last_name`),
  ADD KEY `person_age` (`person_age`),
  ADD KEY `person_nickname` (`person_nickname`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`post_pk`),
  ADD UNIQUE KEY `post_pk` (`post_pk`);

--
-- Indexes for table `trending`
--
ALTER TABLE `trending`
  ADD UNIQUE KEY `trend_pk` (`trend_pk`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_pk`),
  ADD UNIQUE KEY `user_pk` (`user_pk`),
  ADD UNIQUE KEY `user_email` (`user_email`),
  ADD UNIQUE KEY `user_name` (`user_username`),
  ADD KEY `user_first_name` (`user_first_name`),
  ADD KEY `user_last_name` (`user_last_name`),
  ADD KEY `idx_users_verification_key` (`verification_key`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `people`
--
ALTER TABLE `people`
  MODIFY `person_pk` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `post_pk` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `trending`
--
ALTER TABLE `trending`
  MODIFY `trend_pk` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_pk` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
