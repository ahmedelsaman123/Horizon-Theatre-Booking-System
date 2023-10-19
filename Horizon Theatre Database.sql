-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 22, 2023 at 02:35 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `horizon`
--

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `Booking_Reference` varchar(255) NOT NULL,
  `User_ID` int(11) DEFAULT NULL,
  `Show_ID` int(11) DEFAULT NULL,
  `Theatre_ID` int(11) DEFAULT NULL,
  `Total_Price` decimal(5,2) DEFAULT NULL,
  `Booking_Date` date DEFAULT NULL,
  `Number_of_tickets` int(11) DEFAULT NULL,
  `Drive_in_or_Not` enum('Yes','No') DEFAULT 'No'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `city`
--

CREATE TABLE `city` (
  `City_ID` int(11) NOT NULL,
  `City_Name` varchar(255) DEFAULT NULL,
  `Theatre_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `city`
--

INSERT INTO `city` (`City_ID`, `City_Name`, `Theatre_ID`) VALUES
(1, 'Birmingham', 1),
(2, 'Bristol', 2),
(3, 'Cardiff', 3),
(4, 'London', 4),
(5, 'Manchester', 5),
(6, 'Glasgow', 6),
(7, 'Newcastle', 7);

-- --------------------------------------------------------

--
-- Table structure for table `price`
--

CREATE TABLE `price` (
  `City_ID` int(11) DEFAULT NULL,
  `Early_afternoon_Price` decimal(5,2) DEFAULT NULL,
  `Early_afternoon_Time` varchar(20) DEFAULT NULL,
  `Evening_Price` decimal(5,2) DEFAULT NULL,
  `Evening_Time` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `price`
--

INSERT INTO `price` (`City_ID`, `Early_afternoon_Price`, `Early_afternoon_Time`, `Evening_Price`, `Evening_Time`) VALUES
(1, 6.00, '15:00-17:30', 8.00, '18:00-20:30'),
(2, 6.00, '15:00-17:30', 8.00, '18:00-20:30'),
(3, 5.00, '15:00-17:30', 7.00, '18:00-20:30'),
(4, 10.00, '15:00-17:30', 12.00, '18:00-20:30'),
(5, 7.00, '15:00-17:30', 10.00, '18:00-20:30'),
(6, 5.00, '15:00-17:30', 7.00, '18:00-20:30');

-- --------------------------------------------------------

--
-- Table structure for table `report`
--

CREATE TABLE `report` (
  `ID` int(11) NOT NULL,
  `User_ID` varchar(255) DEFAULT NULL,
  `Creating_date_and_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Report_Data` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `shows`
--

CREATE TABLE `shows` (
  `Show_ID` int(11) NOT NULL,
  `Show_Name` varchar(255) DEFAULT NULL,
  `Description` text DEFAULT NULL,
  `Actors` text DEFAULT NULL,
  `Age_Rating` int(11) DEFAULT NULL,
  `Theatre_ID` int(11) DEFAULT NULL,
  `Theatre_Name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `shows`
--

INSERT INTO `shows` (`Show_ID`, `Show_Name`, `Description`, `Actors`, `Age_Rating`, `Theatre_ID`, `Theatre_Name`) VALUES
(1, 'Oppenheimer', 'The narrative of J. Robert Oppenheimer, the remarkable physicist behind the creation of the world\'s first atomic bomb.', 'Cillian Murphy, Robert Downey Jr. ', 18, 1, 'Birmingham Theatre'),
(2, 'The Theory of Everything', 'The story of the most brilliant and celebrated physicist of our time, Stephen Hawking', 'Eddie Redmayne, Felicity Jones', 12, 4, 'London Theatre'),
(3, 'The Social Network', 'The story about the founders of the social-networking website, Facebook', 'Jesse Eisenberg, Andrew Garfield', 13, 2, 'Bristol Theatre'),
(4, 'The Imitation Game', 'During World War II, mathematician Alan Turing tries to crack the enigma code with help from fellow mathematicians', 'Benedict Cumberbatch, Keira Knightley', 12, 6, 'Glasgow Theatre'),
(5, 'A Beautiful Mind', 'The story of John Nash, a brilliant but asocial mathematician', 'Russell Crowe, Jennifer Connelly', 12, 5, 'Manchester Theatre'),
(6, 'Schindler\'s List', 'The true story of Oskar Schindler who managed to save about 1100 Jews from being gassed at Auschwitz during World War II', 'Liam Neeson, Ralph Fiennes', 15, 3, 'Cardiff Theatre');

-- --------------------------------------------------------

--
-- Table structure for table `theatres`
--

CREATE TABLE `theatres` (
  `Theatre_ID` int(11) NOT NULL,
  `Theatre_Name` varchar(255) DEFAULT NULL,
  `City_Name` varchar(255) DEFAULT NULL,
  `City_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `theatres`
--

INSERT INTO `theatres` (`Theatre_ID`, `Theatre_Name`, `City_Name`, `City_ID`) VALUES
(1, 'Birmingham Theatre', 'Birmingham', 1),
(2, 'Bristol Theatre', 'Bristol', 2),
(3, 'Cardiff Theatre', 'Cardiff', 3),
(4, 'London Theatre', 'London', 4),
(5, 'Manchester Theatre', 'Manchester', 5),
(6, 'Glasgow Theatre', 'Glasgow', 6),
(7, 'Newcastle Theatre', 'Newcastle', 7),
(8, 'Liverpool Theatre', 'Liverpool', 8);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `User_ID` int(11) NOT NULL,
  `Username` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`User_ID`, `Username`, `Password`) VALUES
(1, 'manager1', 'pass1'),
(2, 'staff1', 'pass2');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`Booking_Reference`);

--
-- Indexes for table `city`
--
ALTER TABLE `city`
  ADD PRIMARY KEY (`City_ID`);

--
-- Indexes for table `report`
--
ALTER TABLE `report`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `shows`
--
ALTER TABLE `shows`
  ADD PRIMARY KEY (`Show_ID`);

--
-- Indexes for table `theatres`
--
ALTER TABLE `theatres`
  ADD PRIMARY KEY (`Theatre_ID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`User_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
