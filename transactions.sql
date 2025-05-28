-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: labs-mysql-small-scarce-umbrella:3306
-- Generation Time: Feb 11, 2025 at 12:08 PM
-- Server version: 8.0.37
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `transactions`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`%` PROCEDURE `TRANSACTION_JAMES` ()   BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    START TRANSACTION;
    UPDATE BankAccounts
    SET Balance = Balance-1200
    WHERE AccountName = "James";
    UPDATE BankAccounts
    SET Balance = Balance+1200
    WHERE AccountName = "Shoe Shop";
    UPDATE ShoeShop
    SET Stock = Stock-4
    WHERE Product = "Trainers";
    COMMIT;
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `TRANSACTION_JAMES_` ()   BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    START TRANSACTION;
    UPDATE BankAccounts
    SET Balance = Balance-1200
    WHERE AccountName = "James";
    UPDATE BankAccounts
    SET Balance = Balance+1200
    WHERE AccountName = "Shoe Shop";
    UPDATE ShoeShop
    SET Stock = Stock-4
    WHERE Product = "Trainers";
    UPDATE BankAccounts
    SET Balance = Balance-150
    WHERE AccountName = "James";
    COMMIT;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `BankAccounts`
--

CREATE TABLE `BankAccounts` (
  `AccountNumber` varchar(5) NOT NULL,
  `AccountName` varchar(25) NOT NULL,
  `Balance` decimal(8,2) NOT NULL
) ;

--
-- Dumping data for table `BankAccounts`
--

INSERT INTO `BankAccounts` (`AccountNumber`, `AccountName`, `Balance`) VALUES
('B001', 'Rose', 300.00),
('B002', 'James', 145.00),
('B003', 'Shoe Shop', 125400.00),
('B004', 'Corner Shop', 76000.00);

-- --------------------------------------------------------

--
-- Table structure for table `ShoeShop`
--

CREATE TABLE `ShoeShop` (
  `Product` varchar(25) NOT NULL,
  `Stock` int NOT NULL,
  `Price` decimal(8,2) NOT NULL
) ;

--
-- Dumping data for table `ShoeShop`
--

INSERT INTO `ShoeShop` (`Product`, `Stock`, `Price`) VALUES
('Boots', 11, 200.00),
('Brogues', 10, 150.00),
('High heels', 8, 600.00),
('Trainers', 10, 300.00);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `BankAccounts`
--
ALTER TABLE `BankAccounts`
  ADD PRIMARY KEY (`AccountNumber`);

--
-- Indexes for table `ShoeShop`
--
ALTER TABLE `ShoeShop`
  ADD PRIMARY KEY (`Product`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
