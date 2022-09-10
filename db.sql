-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.0.22-community-nt


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


--
-- Create schema vote
--

CREATE DATABASE IF NOT EXISTS vote;
USE vote;

--
-- Definition of table `people`
--

DROP TABLE IF EXISTS `people`;
CREATE TABLE `people` (
  `Id` int(10) unsigned NOT NULL auto_increment,
  `username` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  PRIMARY KEY  (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `people`
--

/*!40000 ALTER TABLE `people` DISABLE KEYS */;
INSERT INTO `people` (`Id`,`username`,`email`,`password`) VALUES 
 (1,'vidhya','santhosh@gmail.com','Sandy@123');
/*!40000 ALTER TABLE `people` ENABLE KEYS */;


--
-- Definition of table `review`
--

DROP TABLE IF EXISTS `review`;
CREATE TABLE `review` (
  `Id` int(10) unsigned NOT NULL auto_increment,
  `news_content` varchar(300) NOT NULL,
  `pred` varchar(45) NOT NULL,
  `userid` varchar(45) NOT NULL,
  `parties_name` varchar(45) NOT NULL,
  PRIMARY KEY  (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `review`
--

/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` (`Id`,`news_content`,`pred`,`userid`,`parties_name`) VALUES 
 (1,'he will lose this election','Negative','1','Republican(Donald Trump)');
/*!40000 ALTER TABLE `review` ENABLE KEYS */;




/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
