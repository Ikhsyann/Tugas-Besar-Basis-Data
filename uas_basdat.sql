-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 10, 2025 at 05:06 AM
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
-- Database: `uas_basdat`
--

-- --------------------------------------------------------

--
-- Table structure for table `kesehatan_mental`
--

CREATE TABLE `kesehatan_mental` (
  `id_kesehatan` int(11) NOT NULL,
  `id_responden` int(11) NOT NULL,
  `gangguan_fokus` tinyint(4) NOT NULL COMMENT 'Distraction:  Skala 1-5',
  `gelisah` tinyint(4) NOT NULL COMMENT 'Restlessness: Skala 1-5',
  `kecemasan` tinyint(4) NOT NULL COMMENT 'Anxiety: Skala 1-5',
  `kesulitan_konsentrasi` tinyint(4) NOT NULL COMMENT 'Concentration Difficulty: Skala 1-5',
  `perbandingan_diri` tinyint(4) NOT NULL COMMENT 'Self Comparison: Skala 1-5',
  `sentimen_posting` tinyint(4) NOT NULL COMMENT 'Post Sentiment: Skala 1-5',
  `mencari_validasi` tinyint(4) NOT NULL COMMENT 'Validation Seeking: Skala 1-5',
  `depresi` tinyint(4) NOT NULL COMMENT 'Depression: Skala 1-5',
  `fluktuasi_minat` tinyint(4) NOT NULL COMMENT 'Activity Interest Variance: Skala 1-5',
  `sulit_tidur` tinyint(4) NOT NULL COMMENT 'Sleeplessness: Skala 1-5'
) ;

--
-- Dumping data for table `kesehatan_mental`
--

INSERT INTO `kesehatan_mental` (`id_kesehatan`, `id_responden`, `gangguan_fokus`, `gelisah`, `kecemasan`, `kesulitan_konsentrasi`, `perbandingan_diri`, `sentimen_posting`, `mencari_validasi`, `depresi`, `fluktuasi_minat`, `sulit_tidur`) VALUES
(1, 1, 4, 3, 3, 4, 2, 3, 2, 3, 4, 4),
(2, 2, 5, 5, 5, 4, 5, 1, 5, 5, 5, 5),
(3, 3, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2),
(4, 4, 5, 4, 4, 5, 4, 2, 4, 4, 5, 5),
(5, 5, 4, 4, 5, 4, 5, 2, 5, 4, 4, 4),
(6, 6, 3, 4, 4, 3, 3, 3, 3, 3, 3, 3),
(7, 7, 1, 1, 2, 1, 1, 4, 1, 1, 1, 1),
(8, 8, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2),
(9, 9, 5, 5, 5, 5, 5, 2, 5, 5, 5, 5),
(10, 10, 2, 2, 3, 2, 2, 3, 2, 2, 2, 3),
(11, 11, 4, 4, 4, 4, 4, 2, 4, 4, 4, 4),
(12, 12, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1),
(13, 13, 3, 2, 3, 2, 3, 3, 2, 2, 2, 3),
(14, 14, 3, 3, 4, 3, 4, 3, 4, 3, 3, 3),
(15, 15, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5),
(16, 16, 3, 3, 3, 3, 2, 3, 2, 2, 3, 3),
(17, 17, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2),
(18, 18, 3, 3, 4, 3, 2, 3, 2, 3, 3, 3),
(19, 19, 4, 4, 4, 4, 5, 2, 5, 4, 4, 4),
(20, 20, 2, 2, 3, 2, 2, 3, 2, 2, 2, 2),
(21, 21, 4, 4, 4, 4, 5, 2, 5, 4, 4, 4),
(22, 22, 4, 3, 3, 4, 2, 3, 2, 3, 4, 4),
(23, 23, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5),
(24, 24, 3, 3, 3, 4, 3, 3, 3, 3, 3, 4),
(25, 25, 4, 4, 4, 4, 4, 2, 4, 4, 4, 4),
(26, 26, 1, 1, 2, 1, 1, 4, 1, 1, 1, 2),
(27, 27, 4, 4, 4, 3, 4, 2, 4, 3, 3, 4),
(28, 28, 3, 3, 3, 3, 2, 3, 2, 2, 3, 3),
(29, 29, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5),
(30, 30, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3),
(31, 31, 1, 1, 2, 1, 1, 4, 1, 1, 1, 2),
(32, 32, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3),
(33, 33, 2, 2, 3, 2, 3, 3, 2, 2, 2, 2),
(34, 34, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2),
(35, 35, 5, 5, 5, 5, 5, 1, 5, 5, 5, 5),
(36, 36, 2, 2, 3, 2, 2, 3, 2, 2, 2, 2),
(37, 37, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2),
(38, 38, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3),
(39, 39, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1),
(40, 40, 4, 4, 4, 3, 4, 2, 4, 3, 3, 4),
(41, 41, 2, 2, 3, 2, 2, 3, 2, 2, 2, 2),
(42, 42, 4, 3, 4, 4, 4, 2, 3, 3, 3, 4),
(43, 43, 1, 1, 2, 1, 1, 4, 1, 1, 1, 2),
(44, 44, 3, 2, 3, 3, 2, 3, 2, 2, 3, 3),
(45, 45, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2),
(46, 46, 3, 3, 4, 3, 2, 3, 2, 3, 3, 3),
(47, 47, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2),
(48, 48, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2),
(49, 49, 3, 3, 4, 3, 4, 3, 4, 3, 3, 3),
(50, 50, 2, 2, 3, 2, 2, 3, 2, 2, 2, 2),
(51, 51, 4, 4, 4, 4, 4, 2, 4, 4, 4, 4),
(52, 52, 2, 2, 3, 2, 2, 3, 2, 2, 2, 2),
(53, 53, 4, 3, 4, 4, 4, 2, 4, 3, 3, 4),
(54, 54, 2, 2, 3, 2, 2, 3, 2, 2, 2, 3),
(55, 55, 4, 4, 5, 4, 5, 2, 5, 4, 4, 4),
(56, 56, 1, 1, 2, 1, 1, 4, 1, 1, 1, 1),
(57, 57, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2),
(58, 58, 3, 3, 3, 3, 2, 3, 2, 3, 3, 3),
(59, 59, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1),
(60, 60, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2),
(61, 61, 2, 2, 3, 2, 2, 3, 2, 2, 2, 2),
(62, 62, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2),
(63, 63, 3, 3, 4, 3, 2, 3, 2, 3, 3, 3),
(64, 64, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3),
(65, 65, 2, 2, 2, 2, 1, 4, 1, 2, 2, 2),
(66, 66, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2),
(67, 67, 3, 2, 3, 3, 2, 3, 2, 2, 3, 3),
(68, 68, 3, 3, 4, 3, 4, 3, 4, 3, 3, 3),
(69, 69, 2, 2, 3, 2, 2, 3, 2, 2, 2, 3),
(70, 70, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2),
(71, 71, 2, 2, 2, 2, 1, 4, 1, 2, 2, 2),
(72, 72, 1, 1, 2, 1, 1, 4, 1, 1, 1, 2),
(73, 73, 2, 2, 2, 2, 1, 4, 1, 2, 2, 2),
(74, 74, 2, 2, 2, 2, 1, 4, 1, 2, 2, 2),
(75, 75, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1),
(76, 76, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2),
(77, 77, 2, 2, 3, 2, 1, 3, 1, 2, 2, 2),
(78, 78, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2),
(79, 79, 2, 2, 2, 2, 1, 4, 1, 2, 2, 2),
(80, 80, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2),
(81, 81, 1, 1, 2, 1, 1, 4, 1, 1, 1, 2),
(82, 82, 2, 2, 2, 2, 1, 4, 1, 2, 2, 2),
(83, 83, 2, 2, 3, 2, 1, 3, 1, 2, 2, 2),
(84, 84, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2),
(85, 85, 2, 2, 2, 2, 1, 4, 1, 2, 2, 2),
(86, 86, 2, 2, 2, 2, 1, 4, 1, 2, 2, 2),
(87, 87, 2, 2, 2, 2, 1, 4, 1, 2, 2, 2),
(88, 88, 1, 1, 2, 1, 1, 4, 1, 1, 1, 2),
(89, 89, 1, 1, 2, 1, 1, 4, 1, 1, 1, 2),
(90, 90, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1),
(91, 91, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1),
(92, 92, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1),
(93, 93, 1, 1, 2, 1, 1, 5, 1, 1, 1, 1),
(94, 94, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1),
(95, 95, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1),
(96, 96, 1, 1, 2, 1, 1, 5, 1, 1, 1, 2),
(97, 97, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1),
(98, 98, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1),
(99, 99, 1, 1, 2, 1, 1, 5, 1, 1, 1, 1),
(100, 100, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `master_platform`
--

CREATE TABLE `master_platform` (
  `id_platform` int(11) NOT NULL,
  `nama_platform` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `master_platform`
--

INSERT INTO `master_platform` (`id_platform`, `nama_platform`) VALUES
(5, 'Discord'),
(1, 'Facebook'),
(3, 'Instagram'),
(8, 'Pinterest'),
(6, 'Reddit'),
(7, 'Snapchat'),
(9, 'TikTok'),
(2, 'Twitter'),
(4, 'YouTube');

-- --------------------------------------------------------

--
-- Table structure for table `penggunaan_per_platform`
--

CREATE TABLE `penggunaan_per_platform` (
  `id_penggunaan` int(11) NOT NULL,
  `id_responden` int(11) NOT NULL,
  `id_platform` int(11) NOT NULL,
  `jam_per_hari` decimal(3,1) NOT NULL COMMENT 'Jam penggunaan per hari (0. 1 - 24.0)',
  `tujuan_penggunaan` enum('Hiburan','Komunikasi','Informasi','Pekerjaan','Lainnya') NOT NULL,
  `frekuensi_buka_per_hari` tinyint(4) NOT NULL COMMENT 'Berapa kali membuka aplikasi per hari'
) ;

--
-- Dumping data for table `penggunaan_per_platform`
--

INSERT INTO `penggunaan_per_platform` (`id_penggunaan`, `id_responden`, `id_platform`, `jam_per_hari`, `tujuan_penggunaan`, `frekuensi_buka_per_hari`) VALUES
(1, 1, 5, 7.5, 'Hiburan', 45),
(2, 1, 4, 4.5, 'Hiburan', 15),
(3, 1, 6, 2.0, 'Informasi', 10),
(4, 2, 3, 6.5, 'Hiburan', 55),
(5, 2, 9, 4.0, 'Hiburan', 40),
(6, 2, 4, 2.5, 'Informasi', 8),
(7, 2, 8, 1.5, 'Hiburan', 12),
(8, 3, 3, 2.5, 'Komunikasi', 12),
(9, 3, 1, 1.5, 'Komunikasi', 8),
(10, 3, 4, 1.0, 'Informasi', 4),
(11, 4, 9, 8.0, 'Hiburan', 60),
(12, 4, 3, 3.5, 'Komunikasi', 25),
(13, 4, 4, 2.0, 'Hiburan', 10),
(14, 5, 3, 5.5, 'Hiburan', 48),
(15, 5, 8, 3.0, 'Hiburan', 20),
(16, 5, 9, 2.5, 'Hiburan', 18),
(17, 6, 2, 5.0, 'Informasi', 40),
(18, 6, 6, 3.5, 'Informasi', 25),
(19, 6, 3, 2.0, 'Komunikasi', 10),
(20, 7, 3, 1.5, 'Komunikasi', 8),
(21, 7, 4, 1.0, 'Informasi', 4),
(22, 8, 4, 4.5, 'Informasi', 12),
(23, 8, 6, 2.5, 'Informasi', 15),
(24, 8, 3, 1.5, 'Komunikasi', 8),
(25, 9, 3, 4.5, 'Komunikasi', 50),
(26, 9, 9, 3.5, 'Hiburan', 45),
(27, 9, 1, 2.5, 'Komunikasi', 30),
(28, 9, 2, 2.0, 'Informasi', 25),
(29, 10, 6, 5.0, 'Informasi', 30),
(30, 10, 4, 3.0, 'Hiburan', 10),
(31, 10, 2, 1.5, 'Informasi', 12),
(32, 11, 3, 4.0, 'Hiburan', 35),
(33, 11, 9, 3.5, 'Hiburan', 30),
(34, 11, 1, 3.0, 'Komunikasi', 25),
(35, 11, 4, 2.5, 'Hiburan', 12),
(36, 11, 2, 2.0, 'Informasi', 15),
(37, 12, 3, 1.0, 'Komunikasi', 5),
(38, 12, 4, 0.5, 'Informasi', 2),
(39, 13, 8, 4.5, 'Hiburan', 25),
(40, 13, 3, 2.5, 'Komunikasi', 15),
(41, 13, 4, 2.0, 'Informasi', 8),
(42, 14, 7, 5.0, 'Komunikasi', 40),
(43, 14, 3, 3.0, 'Komunikasi', 20),
(44, 14, 9, 2.5, 'Hiburan', 18),
(45, 15, 3, 5.5, 'Komunikasi', 60),
(46, 15, 9, 4.0, 'Hiburan', 50),
(47, 15, 2, 3.0, 'Informasi', 35),
(48, 15, 1, 2.5, 'Komunikasi', 28),
(49, 16, 5, 6.5, 'Komunikasi', 40),
(50, 16, 4, 3.5, 'Hiburan', 12),
(51, 16, 6, 2.0, 'Informasi', 10),
(52, 17, 3, 2.0, 'Komunikasi', 10),
(53, 17, 4, 1.5, 'Informasi', 6),
(54, 17, 1, 1.0, 'Komunikasi', 5),
(55, 18, 2, 4.5, 'Informasi', 30),
(56, 18, 6, 3.5, 'Informasi', 20),
(57, 18, 4, 2.0, 'Informasi', 8),
(58, 19, 9, 7.0, 'Hiburan', 50),
(59, 19, 3, 4.0, 'Komunikasi', 30),
(60, 19, 4, 2.5, 'Informasi', 10),
(61, 20, 3, 2.5, 'Komunikasi', 12),
(62, 20, 4, 2.0, 'Informasi', 8),
(63, 20, 1, 1.5, 'Komunikasi', 8),
(64, 21, 9, 6.5, 'Hiburan', 55),
(65, 21, 3, 3.5, 'Komunikasi', 28),
(66, 21, 7, 2.0, 'Komunikasi', 15),
(67, 22, 5, 8.0, 'Hiburan', 50),
(68, 22, 4, 4.0, 'Hiburan', 15),
(69, 22, 9, 2.5, 'Hiburan', 20),
(70, 23, 3, 6.0, 'Komunikasi', 65),
(71, 23, 7, 3.5, 'Komunikasi', 35),
(72, 23, 9, 2.5, 'Hiburan', 22),
(73, 24, 4, 7.5, 'Hiburan', 25),
(74, 24, 9, 3.0, 'Hiburan', 28),
(75, 24, 3, 2.0, 'Komunikasi', 12),
(76, 25, 3, 4.5, 'Hiburan', 40),
(77, 25, 9, 4.0, 'Hiburan', 38),
(78, 25, 1, 2.5, 'Komunikasi', 20),
(79, 25, 4, 2.0, 'Hiburan', 10),
(80, 26, 3, 1.5, 'Komunikasi', 8),
(81, 26, 4, 1.0, 'Informasi', 4),
(82, 27, 7, 5.5, 'Komunikasi', 50),
(83, 27, 3, 3.5, 'Komunikasi', 30),
(84, 27, 9, 2.0, 'Hiburan', 18),
(85, 28, 5, 7.0, 'Komunikasi', 45),
(86, 28, 4, 3.5, 'Hiburan', 12),
(87, 28, 6, 1.5, 'Informasi', 8),
(88, 29, 3, 5.5, 'Komunikasi', 70),
(89, 29, 9, 5.0, 'Hiburan', 60),
(90, 29, 7, 3.5, 'Komunikasi', 45),
(91, 29, 1, 2.5, 'Komunikasi', 25),
(92, 30, 3, 3.0, 'Komunikasi', 18),
(93, 30, 9, 2.5, 'Hiburan', 20),
(94, 30, 4, 1.5, 'Hiburan', 8),
(95, 31, 3, 1.5, 'Komunikasi', 8),
(96, 31, 4, 1.0, 'Informasi', 5),
(97, 32, 2, 4.5, 'Hiburan', 35),
(98, 32, 9, 3.0, 'Hiburan', 25),
(99, 32, 3, 2.0, 'Komunikasi', 12),
(100, 33, 8, 4.0, 'Hiburan', 22),
(101, 33, 3, 2.5, 'Komunikasi', 15),
(102, 33, 4, 1.5, 'Informasi', 8),
(103, 34, 4, 5.0, 'Informasi', 15),
(104, 34, 6, 2.5, 'Informasi', 12),
(105, 34, 3, 1.5, 'Komunikasi', 8),
(106, 35, 3, 7.0, 'Hiburan', 70),
(107, 35, 9, 4.5, 'Hiburan', 50),
(108, 35, 8, 2.5, 'Hiburan', 20),
(109, 35, 7, 2.0, 'Komunikasi', 18),
(110, 36, 3, 2.0, 'Pekerjaan', 12),
(111, 36, 2, 1.5, 'Informasi', 10),
(112, 36, 4, 1.0, 'Informasi', 5),
(113, 37, 3, 2.5, 'Komunikasi', 14),
(114, 37, 1, 1.5, 'Komunikasi', 10),
(115, 37, 4, 1.0, 'Hiburan', 5),
(116, 38, 3, 3.5, 'Komunikasi', 22),
(117, 38, 1, 2.5, 'Komunikasi', 18),
(118, 38, 8, 2.0, 'Hiburan', 12),
(119, 39, 1, 1.5, 'Komunikasi', 8),
(120, 39, 4, 0.5, 'Informasi', 3),
(121, 40, 3, 4.0, 'Hiburan', 30),
(122, 40, 8, 2.5, 'Hiburan', 18),
(123, 40, 9, 2.0, 'Hiburan', 15),
(124, 41, 2, 2.5, 'Informasi', 15),
(125, 41, 6, 1.5, 'Informasi', 12),
(126, 41, 4, 1.0, 'Informasi', 5),
(127, 42, 3, 3.5, 'Hiburan', 25),
(128, 42, 9, 3.0, 'Hiburan', 22),
(129, 42, 4, 2.0, 'Hiburan', 10),
(130, 43, 1, 1.5, 'Komunikasi', 10),
(131, 43, 3, 1.0, 'Komunikasi', 8),
(132, 44, 5, 4.0, 'Hiburan', 20),
(133, 44, 4, 2.5, 'Hiburan', 10),
(134, 44, 6, 1.5, 'Informasi', 8),
(135, 45, 8, 3.0, 'Informasi', 18),
(136, 45, 1, 2.0, 'Komunikasi', 12),
(137, 45, 3, 1.5, 'Komunikasi', 10),
(138, 46, 2, 3.5, 'Informasi', 25),
(139, 46, 6, 2.0, 'Informasi', 15),
(140, 46, 4, 1.5, 'Informasi', 8),
(141, 47, 1, 2.5, 'Komunikasi', 15),
(142, 47, 4, 1.0, 'Informasi', 5),
(143, 48, 4, 3.5, 'Informasi', 12),
(144, 48, 6, 2.0, 'Informasi', 10),
(145, 48, 3, 1.0, 'Komunikasi', 6),
(146, 49, 3, 3.5, 'Hiburan', 28),
(147, 49, 8, 2.0, 'Hiburan', 15),
(148, 49, 9, 1.5, 'Hiburan', 12),
(149, 50, 5, 4.5, 'Komunikasi', 30),
(150, 50, 6, 2.5, 'Informasi', 15),
(151, 50, 4, 1.5, 'Hiburan', 8),
(152, 51, 3, 4.0, 'Hiburan', 35),
(153, 51, 9, 3.5, 'Hiburan', 30),
(154, 51, 2, 2.5, 'Informasi', 20),
(155, 51, 1, 2.0, 'Komunikasi', 15),
(156, 52, 3, 2.5, 'Komunikasi', 15),
(157, 52, 4, 2.0, 'Informasi', 10),
(158, 52, 1, 1.5, 'Komunikasi', 10),
(159, 53, 9, 4.5, 'Hiburan', 40),
(160, 53, 3, 2.5, 'Komunikasi', 18),
(161, 53, 4, 1.5, 'Hiburan', 8),
(162, 54, 6, 4.0, 'Informasi', 25),
(163, 54, 4, 2.5, 'Informasi', 10),
(164, 54, 2, 1.5, 'Informasi', 12),
(165, 55, 3, 5.0, 'Hiburan', 45),
(166, 55, 9, 3.0, 'Hiburan', 28),
(167, 55, 8, 2.0, 'Hiburan', 15),
(168, 56, 1, 1.5, 'Komunikasi', 10),
(169, 56, 3, 1.0, 'Komunikasi', 8),
(170, 57, 1, 2.0, 'Komunikasi', 12),
(171, 57, 3, 1.5, 'Komunikasi', 10),
(172, 57, 4, 0.5, 'Informasi', 3),
(173, 58, 5, 5.5, 'Hiburan', 35),
(174, 58, 4, 3.0, 'Hiburan', 12),
(175, 58, 6, 2.0, 'Informasi', 10),
(176, 59, 1, 1.0, 'Komunikasi', 6),
(177, 59, 4, 0.5, 'Informasi', 3),
(178, 60, 4, 3.0, 'Hiburan', 12),
(179, 60, 6, 1.5, 'Informasi', 8),
(180, 61, 3, 2.5, 'Komunikasi', 15),
(181, 61, 1, 2.0, 'Komunikasi', 12),
(182, 61, 4, 1.5, 'Informasi', 8),
(183, 62, 1, 3.0, 'Komunikasi', 20),
(184, 62, 4, 1.5, 'Informasi', 8),
(185, 62, 8, 1.0, 'Hiburan', 6),
(186, 63, 2, 3.5, 'Informasi', 28),
(187, 63, 6, 2.0, 'Informasi', 15),
(188, 63, 4, 1.0, 'Informasi', 6),
(189, 64, 8, 3.5, 'Hiburan', 22),
(190, 64, 3, 2.5, 'Komunikasi', 15),
(191, 64, 9, 1.5, 'Hiburan', 10),
(192, 65, 2, 2.0, 'Pekerjaan', 12),
(193, 65, 4, 1.0, 'Pekerjaan', 5),
(194, 66, 3, 2.0, 'Komunikasi', 12),
(195, 66, 4, 1.5, 'Informasi', 8),
(196, 66, 1, 1.0, 'Komunikasi', 6),
(197, 67, 5, 4.0, 'Hiburan', 25),
(198, 67, 4, 2.5, 'Hiburan', 10),
(199, 67, 6, 1.5, 'Informasi', 8),
(200, 68, 3, 3.0, 'Komunikasi', 25),
(201, 68, 7, 2.0, 'Komunikasi', 18),
(202, 68, 9, 1.5, 'Hiburan', 12),
(203, 69, 6, 4.5, 'Informasi', 30),
(204, 69, 2, 2.5, 'Informasi', 18),
(205, 69, 4, 2.0, 'Informasi', 10),
(206, 70, 3, 1.5, 'Komunikasi', 10),
(207, 70, 1, 1.0, 'Komunikasi', 8),
(208, 70, 4, 0.5, 'Informasi', 4),
(209, 71, 1, 2.0, 'Informasi', 12),
(210, 71, 4, 1.5, 'Informasi', 8),
(211, 72, 1, 1.5, 'Komunikasi', 10),
(212, 72, 3, 0.5, 'Komunikasi', 4),
(213, 73, 4, 2.5, 'Hiburan', 10),
(214, 73, 1, 1.0, 'Komunikasi', 6),
(215, 74, 1, 2.0, 'Komunikasi', 12),
(216, 74, 4, 1.0, 'Informasi', 5),
(217, 75, 1, 1.0, 'Komunikasi', 6),
(218, 75, 4, 0.5, 'Informasi', 3),
(219, 76, 3, 1.5, 'Komunikasi', 10),
(220, 76, 1, 1.0, 'Komunikasi', 6),
(221, 77, 2, 2.0, 'Informasi', 12),
(222, 77, 4, 1.5, 'Informasi', 8),
(223, 78, 1, 2.5, 'Komunikasi', 15),
(224, 78, 8, 1.0, 'Hiburan', 6),
(225, 79, 4, 2.0, 'Informasi', 10),
(226, 79, 1, 1.0, 'Komunikasi', 6),
(227, 80, 1, 1.5, 'Komunikasi', 8),
(228, 80, 3, 1.0, 'Komunikasi', 6),
(229, 81, 1, 1.0, 'Komunikasi', 5),
(230, 81, 4, 0.5, 'Informasi', 3),
(231, 82, 1, 1.5, 'Komunikasi', 10),
(232, 82, 4, 0.5, 'Informasi', 4),
(233, 83, 2, 2.0, 'Informasi', 15),
(234, 83, 4, 1.0, 'Informasi', 6),
(235, 84, 8, 2.5, 'Informasi', 15),
(236, 84, 1, 1.5, 'Komunikasi', 10),
(237, 85, 4, 2.5, 'Informasi', 12),
(238, 85, 6, 1.0, 'Informasi', 6),
(239, 86, 1, 1.5, 'Komunikasi', 8),
(240, 86, 4, 1.0, 'Informasi', 5),
(241, 87, 2, 1.5, 'Informasi', 10),
(242, 87, 4, 1.0, 'Informasi', 6),
(243, 88, 1, 1.5, 'Komunikasi', 10),
(244, 88, 3, 0.5, 'Komunikasi', 4),
(245, 89, 1, 1.0, 'Komunikasi', 6),
(246, 89, 4, 0.5, 'Informasi', 3),
(247, 90, 1, 1.0, 'Komunikasi', 5),
(248, 90, 4, 0.5, 'Informasi', 2);

-- --------------------------------------------------------

--
-- Table structure for table `responden`
--

CREATE TABLE `responden` (
  `id_responden` int(11) NOT NULL,
  `nama` varchar(100) DEFAULT NULL COMMENT 'Nama responden (opsional)',
  `usia` int(11) NOT NULL COMMENT 'Usia dalam tahun',
  `jenis_kelamin` enum('Laki-laki','Perempuan') NOT NULL,
  `status_hubungan` enum('Belum Kawin','Kawin','Cerai Hidup','Cerai Mati') NOT NULL,
  `pekerjaan` enum('Mahasiswa','Pelajar','Pekerja','Pensiunan') NOT NULL,
  `menggunakan_medsos` enum('Ya','Tidak') NOT NULL DEFAULT 'Ya'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `responden`
--

INSERT INTO `responden` (`id_responden`, `nama`, `usia`, `jenis_kelamin`, `status_hubungan`, `pekerjaan`, `menggunakan_medsos`) VALUES
(1, 'Adi Nugroho', 20, 'Laki-laki', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(2, 'Bella Kusuma', 21, 'Perempuan', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(3, 'Citra Maharani', 22, 'Perempuan', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(4, 'Dimas Pratama', 19, 'Laki-laki', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(5, 'Elisa Putri', 21, 'Perempuan', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(6, 'Fahmi Rahman', 23, 'Laki-laki', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(7, 'Gina Puspita', 20, 'Perempuan', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(8, 'Hendra Wijaya', 22, 'Laki-laki', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(9, 'Indah Sari', 21, 'Perempuan', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(10, 'Joko Santoso', 20, 'Laki-laki', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(11, 'Kartika Dewi', 22, 'Perempuan', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(12, 'Lukman Hakim', 23, 'Laki-laki', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(13, 'Maya Anggun', 21, 'Perempuan', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(14, 'Nanda Kusuma', 20, 'Laki-laki', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(15, 'Olivia Permata', 22, 'Perempuan', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(16, 'Pandu Saputra', 21, 'Laki-laki', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(17, 'Qory Amalia', 20, 'Perempuan', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(18, 'Rizki Firmansyah', 23, 'Laki-laki', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(19, 'Sinta Maharani', 21, 'Perempuan', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(20, 'Teguh Prasetyo', 22, 'Laki-laki', 'Belum Kawin', 'Mahasiswa', 'Ya'),
(21, 'Umi Kalsum', 17, 'Perempuan', 'Belum Kawin', 'Pelajar', 'Ya'),
(22, 'Vicky Maulana', 18, 'Laki-laki', 'Belum Kawin', 'Pelajar', 'Ya'),
(23, 'Winda Sari', 17, 'Perempuan', 'Belum Kawin', 'Pelajar', 'Ya'),
(24, 'Xavier Kurniawan', 18, 'Laki-laki', 'Belum Kawin', 'Pelajar', 'Ya'),
(25, 'Yanti Puspita', 17, 'Perempuan', 'Belum Kawin', 'Pelajar', 'Ya'),
(26, 'Zainal Abidin', 18, 'Laki-laki', 'Belum Kawin', 'Pelajar', 'Ya'),
(27, 'Ayu Lestari', 17, 'Perempuan', 'Belum Kawin', 'Pelajar', 'Ya'),
(28, 'Bambang Susilo', 18, 'Laki-laki', 'Belum Kawin', 'Pelajar', 'Ya'),
(29, 'Cindy Wijaya', 17, 'Perempuan', 'Belum Kawin', 'Pelajar', 'Ya'),
(30, 'Dedi Kurniawan', 18, 'Laki-laki', 'Belum Kawin', 'Pelajar', 'Ya'),
(31, 'Erna Puspita', 17, 'Perempuan', 'Belum Kawin', 'Pelajar', 'Ya'),
(32, 'Faisal Rahman', 18, 'Laki-laki', 'Belum Kawin', 'Pelajar', 'Ya'),
(33, 'Gita Maharani', 17, 'Perempuan', 'Belum Kawin', 'Pelajar', 'Ya'),
(34, 'Hendra Saputra', 18, 'Laki-laki', 'Belum Kawin', 'Pelajar', 'Ya'),
(35, 'Intan Permata', 17, 'Perempuan', 'Belum Kawin', 'Pelajar', 'Ya'),
(36, 'Jansen Simanjuntak', 25, 'Laki-laki', 'Belum Kawin', 'Pekerja', 'Ya'),
(37, 'Kurnia Dewi', 26, 'Perempuan', 'Belum Kawin', 'Pekerja', 'Ya'),
(38, 'Linda Wijayanti', 27, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(39, 'Martin Hutabarat', 28, 'Laki-laki', 'Kawin', 'Pekerja', 'Ya'),
(40, 'Novita Sari', 25, 'Perempuan', 'Belum Kawin', 'Pekerja', 'Ya'),
(41, 'Oscar Panjaitan', 29, 'Laki-laki', 'Kawin', 'Pekerja', 'Ya'),
(42, 'Priska Amalia', 26, 'Perempuan', 'Belum Kawin', 'Pekerja', 'Ya'),
(43, 'Qonita Rahman', 30, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(44, 'Rudi Hartono', 27, 'Laki-laki', 'Belum Kawin', 'Pekerja', 'Ya'),
(45, 'Siska Melani', 28, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(46, 'Taufik Hidayat', 25, 'Laki-laki', 'Belum Kawin', 'Pekerja', 'Ya'),
(47, 'Ulfa Nurjanah', 31, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(48, 'Vero Sinaga', 26, 'Laki-laki', 'Belum Kawin', 'Pekerja', 'Ya'),
(49, 'Wulan Dari', 29, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(50, 'Yoga Pratama', 27, 'Laki-laki', 'Belum Kawin', 'Pekerja', 'Ya'),
(51, 'Zahra Amelia', 25, 'Perempuan', 'Belum Kawin', 'Pekerja', 'Ya'),
(52, 'Arief Budiman', 30, 'Laki-laki', 'Kawin', 'Pekerja', 'Ya'),
(53, 'Bunga Citra', 26, 'Perempuan', 'Belum Kawin', 'Pekerja', 'Ya'),
(54, 'Candra Kirana', 28, 'Laki-laki', 'Kawin', 'Pekerja', 'Ya'),
(55, 'Dina Mariana', 25, 'Perempuan', 'Belum Kawin', 'Pekerja', 'Ya'),
(56, 'Eko Prasetyo', 31, 'Laki-laki', 'Kawin', 'Pekerja', 'Ya'),
(57, 'Fitri Anggraini', 27, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(58, 'Gilang Ramadhan', 26, 'Laki-laki', 'Belum Kawin', 'Pekerja', 'Ya'),
(59, 'Hesty Nuraini', 29, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(60, 'Irfan Maulana', 28, 'Laki-laki', 'Kawin', 'Pekerja', 'Ya'),
(61, 'Julia Safitri', 25, 'Perempuan', 'Belum Kawin', 'Pekerja', 'Ya'),
(62, 'Kartika Sari', 30, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(63, 'Lukman Hakim', 27, 'Laki-laki', 'Belum Kawin', 'Pekerja', 'Ya'),
(64, 'Maya Kusuma', 26, 'Perempuan', 'Belum Kawin', 'Pekerja', 'Ya'),
(65, 'Nanda Pratama', 31, 'Laki-laki', 'Kawin', 'Pekerja', 'Ya'),
(66, 'Olivia Permata', 28, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(67, 'Pandu Wijaya', 25, 'Laki-laki', 'Belum Kawin', 'Pekerja', 'Ya'),
(68, 'Qory Sandrina', 29, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(69, 'Rizki Firmansyah', 27, 'Laki-laki', 'Belum Kawin', 'Pekerja', 'Ya'),
(70, 'Sinta Dewi', 30, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(71, 'Teguh Santoso', 35, 'Laki-laki', 'Kawin', 'Pekerja', 'Ya'),
(72, 'Umi Kalsum', 36, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(73, 'Vicky Prasetyo', 38, 'Laki-laki', 'Kawin', 'Pekerja', 'Ya'),
(74, 'Winda Sari', 37, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(75, 'Xavier Nugroho', 39, 'Laki-laki', 'Kawin', 'Pekerja', 'Ya'),
(76, 'Yanti Kusuma', 35, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(77, 'Zainal Abidin', 40, 'Laki-laki', 'Kawin', 'Pekerja', 'Ya'),
(78, 'Ayu Lestari', 36, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(79, 'Bambang Susilo', 41, 'Laki-laki', 'Kawin', 'Pekerja', 'Ya'),
(80, 'Cindy Wijaya', 38, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(81, 'Dedi Kurniawan', 42, 'Laki-laki', 'Kawin', 'Pekerja', 'Ya'),
(82, 'Erna Puspita', 37, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(83, 'Faisal Rahman', 39, 'Laki-laki', 'Kawin', 'Pekerja', 'Ya'),
(84, 'Gita Maharani', 35, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(85, 'Hendra Saputra', 43, 'Laki-laki', 'Kawin', 'Pekerja', 'Ya'),
(86, 'Intan Permata', 36, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(87, 'Jansen Simanjuntak', 40, 'Laki-laki', 'Kawin', 'Pekerja', 'Ya'),
(88, 'Kurnia Dewi', 38, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(89, 'Linda Wijayanti', 44, 'Perempuan', 'Kawin', 'Pekerja', 'Ya'),
(90, 'Martin Hutabarat', 41, 'Laki-laki', 'Kawin', 'Pekerja', 'Ya'),
(91, 'Novita Sari', 45, 'Perempuan', 'Kawin', 'Pekerja', 'Tidak'),
(92, 'Oscar Panjaitan', 42, 'Laki-laki', 'Kawin', 'Pekerja', 'Tidak'),
(93, 'Priska Amalia', 43, 'Perempuan', 'Kawin', 'Pekerja', 'Tidak'),
(94, 'Qonita Rahman', 44, 'Perempuan', 'Kawin', 'Pekerja', 'Tidak'),
(95, 'Rudi Hartono', 45, 'Laki-laki', 'Kawin', 'Pekerja', 'Tidak'),
(96, 'Siska Melani', 41, 'Perempuan', 'Kawin', 'Pekerja', 'Tidak'),
(97, 'Taufik Hidayat', 42, 'Laki-laki', 'Kawin', 'Pekerja', 'Tidak'),
(98, 'Ulfa Nurjanah', 43, 'Perempuan', 'Kawin', 'Pekerja', 'Tidak'),
(99, 'Vero Sinaga', 44, 'Laki-laki', 'Kawin', 'Pekerja', 'Tidak'),
(100, 'Wulan Dari', 45, 'Perempuan', 'Kawin', 'Pekerja', 'Tidak');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `kesehatan_mental`
--
ALTER TABLE `kesehatan_mental`
  ADD PRIMARY KEY (`id_kesehatan`),
  ADD UNIQUE KEY `unique_responden_kesehatan` (`id_responden`),
  ADD KEY `idx_depresi` (`depresi`),
  ADD KEY `idx_kecemasan` (`kecemasan`),
  ADD KEY `idx_sulit_tidur` (`sulit_tidur`);

--
-- Indexes for table `master_platform`
--
ALTER TABLE `master_platform`
  ADD PRIMARY KEY (`id_platform`),
  ADD UNIQUE KEY `nama_platform` (`nama_platform`);

--
-- Indexes for table `penggunaan_per_platform`
--
ALTER TABLE `penggunaan_per_platform`
  ADD PRIMARY KEY (`id_penggunaan`),
  ADD UNIQUE KEY `unique_responden_platform` (`id_responden`,`id_platform`),
  ADD KEY `idx_responden` (`id_responden`),
  ADD KEY `idx_platform` (`id_platform`),
  ADD KEY `idx_jam_per_hari` (`jam_per_hari`),
  ADD KEY `idx_tujuan` (`tujuan_penggunaan`);

--
-- Indexes for table `responden`
--
ALTER TABLE `responden`
  ADD PRIMARY KEY (`id_responden`),
  ADD KEY `idx_jenis_kelamin` (`jenis_kelamin`),
  ADD KEY `idx_pekerjaan` (`pekerjaan`),
  ADD KEY `idx_usia` (`usia`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `kesehatan_mental`
--
ALTER TABLE `kesehatan_mental`
  MODIFY `id_kesehatan` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `master_platform`
--
ALTER TABLE `master_platform`
  MODIFY `id_platform` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `penggunaan_per_platform`
--
ALTER TABLE `penggunaan_per_platform`
  MODIFY `id_penggunaan` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `responden`
--
ALTER TABLE `responden`
  MODIFY `id_responden` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `kesehatan_mental`
--
ALTER TABLE `kesehatan_mental`
  ADD CONSTRAINT `fk_kesehatan_responden` FOREIGN KEY (`id_responden`) REFERENCES `responden` (`id_responden`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `penggunaan_per_platform`
--
ALTER TABLE `penggunaan_per_platform`
  ADD CONSTRAINT `fk_penggunaan_platform` FOREIGN KEY (`id_platform`) REFERENCES `master_platform` (`id_platform`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_penggunaan_responden` FOREIGN KEY (`id_responden`) REFERENCES `responden` (`id_responden`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
