-- MySQL dump 10.11
--
-- Host: 192.168.2.50    Database: isk2
-- ------------------------------------------------------
-- Server version	5.0.32-Debian_7etch1-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `author`
--

DROP TABLE IF EXISTS `author`;
CREATE TABLE `author` (
  `title_id` int(11) default NULL,
  `author_name` varchar(255) default NULL,
  `id` int(11) NOT NULL auto_increment,
  PRIMARY KEY  (`id`),
  KEY `title_id` (`title_id`),
  FULLTEXT KEY `author_name` (`author_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `author_title`
--

DROP TABLE IF EXISTS `author_title`;
CREATE TABLE `author_title` (
  `author_id` int(11) default NULL,
  `title_id` int(11) default NULL,
  `id` int(11) NOT NULL auto_increment,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
CREATE TABLE `book` (
  `id` int(11) NOT NULL auto_increment,
  `listprice` float default NULL,
  `consignment_status` varchar(255) default NULL,
  `inventoried_when` date default NULL,
  `type` varchar(50) default NULL,
  `location` varchar(50) default NULL,
  `status` varchar(255) default NULL,
  `distributor` text,
  `title_id` int(11) default NULL,
  `sold_when` date default NULL,
  `halfoff` float default NULL,
  `owner` varchar(255) default NULL,
  `notes` varchar(255) default NULL,
  PRIMARY KEY  (`id`),
  KEY `status` (`status`),
  KEY `title_id` (`title_id`),
  FULLTEXT KEY `distributor` (`distributor`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `cashbox`
--

DROP TABLE IF EXISTS `cashbox`;
CREATE TABLE `cashbox` (
  `amount` float default NULL,
  `date` datetime default NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `title_id` int(11) default NULL,
  `category_name` varchar(255) default NULL,
  `id` int(11) NOT NULL auto_increment,
  PRIMARY KEY  (`id`),
  KEY `title_id` (`title_id`),
  KEY `category_name` (`category_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `emprunt`
--

DROP TABLE IF EXISTS `emprunt`;
CREATE TABLE `emprunt` (
  `id` int(11) NOT NULL auto_increment,
  `item_id` int(11) default NULL,
  `borrower_id` int(11) default NULL,
  `date` datetime default NULL,
  `return_date` datetime default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `kind`
--

DROP TABLE IF EXISTS `kind`;
CREATE TABLE `kind` (
  `kind_name` varchar(255) default NULL,
  `id` int(11) NOT NULL auto_increment,
  `kind_id` int(11) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
CREATE TABLE `member` (
  `id` int(11) NOT NULL auto_increment,
  `first_name` varchar(255) default NULL,
  `last_name` varchar(255) default NULL,
  `e_mail` varchar(255) default NULL,
  `phone` varchar(15) default NULL,
  `paid` varchar(5) default NULL,
  PRIMARY KEY  (`id`),
  KEY `e_mail` (`e_mail`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `notes`
--

DROP TABLE IF EXISTS `notes`;
CREATE TABLE `notes` (
  `message` text,
  `author` varchar(32) default NULL,
  `whenEntered` datetime default NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `title`
--

DROP TABLE IF EXISTS `title`;
CREATE TABLE `title` (
  `id` int(11) NOT NULL auto_increment,
  `isbn` varchar(20) default NULL,
  `booktitle` text,
  `publisher` text,
  `release_date` varchar(255) default NULL,
  `tag` text,
  `type_id` int(11) default NULL,
  `kind_id` int(11) default NULL,
  PRIMARY KEY  (`id`),
  KEY `isbn` (`isbn`),
  FULLTEXT KEY `booktitle` (`booktitle`),
  FULLTEXT KEY `publisher` (`publisher`),
  FULLTEXT KEY `tag` (`tag`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `transactionLog`
--

DROP TABLE IF EXISTS `transactionLog`;
CREATE TABLE `transactionLog` (
  `id` int(11) NOT NULL auto_increment,
  `action` varchar(255) default NULL,
  `amount` float default NULL,
  `date` datetime default NULL,
  `cashier` varchar(255) default NULL,
  `info` text,
  `schedule` varchar(255) default NULL,
  `owner` varchar(255) default NULL,
  `paid_how` varchar(20) default NULL,
  PRIMARY KEY  (`id`),
  FULLTEXT KEY `info` (`info`),
  FULLTEXT KEY `owner` (`owner`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `type`
--

DROP TABLE IF EXISTS `type`;
CREATE TABLE `type` (
  `type_name` varchar(255) default NULL,
  `id` int(11) NOT NULL auto_increment,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2007-08-07 15:02:15
