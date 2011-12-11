-- MySQL dump 9.11
--
-- Host: localhost    Database: infoshop
-- ------------------------------------------------------
-- Server version	4.0.24_Debian-5-log

--
-- Table structure for table `author`
--

CREATE TABLE `author` (
  `title_id` int(11) default NULL,
  `author_name` varchar(255) default NULL,
  `id` int(11) NOT NULL auto_increment,
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;

--
-- Dumping data for table `author`
--

INSERT INTO `author` VALUES (12,'Kim Stanley Robinson',3);

--
-- Table structure for table `book`
--

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
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;

--
-- Dumping data for table `book`
--

INSERT INTO `book` VALUES (5,7.99,NULL,'2005-07-31',NULL,NULL,'STOCK','bt',12);
INSERT INTO `book` VALUES (6,7.99,NULL,'2005-07-31',NULL,NULL,'STOCK','bt',12);

--
-- Table structure for table `cashbox`
--

CREATE TABLE `cashbox` (
  `amount` float default NULL,
  `date` datetime default NULL
) TYPE=MyISAM;

--
-- Dumping data for table `cashbox`
--

INSERT INTO `cashbox` VALUES (1,'2005-05-18 17:52:28');
INSERT INTO `cashbox` VALUES (1,'2005-05-18 18:38:47');
INSERT INTO `cashbox` VALUES (1,'2005-05-18 18:39:46');
INSERT INTO `cashbox` VALUES (1,'2005-05-18 18:42:23');
INSERT INTO `cashbox` VALUES (1,'2005-05-18 19:00:01');
INSERT INTO `cashbox` VALUES (1,'2005-05-18 19:01:14');
INSERT INTO `cashbox` VALUES (1,'2005-05-18 19:04:04');
INSERT INTO `cashbox` VALUES (1,'2005-05-18 19:05:28');
INSERT INTO `cashbox` VALUES (1,'2005-05-18 19:07:54');
INSERT INTO `cashbox` VALUES (1,'2005-05-18 19:09:25');
INSERT INTO `cashbox` VALUES (1.5105,'2005-05-18 19:09:47');
INSERT INTO `cashbox` VALUES (1.51,'2005-05-18 19:11:05');
INSERT INTO `cashbox` VALUES (1.51,'2005-05-18 19:11:48');
INSERT INTO `cashbox` VALUES (1.51,'2005-05-18 19:13:49');
INSERT INTO `cashbox` VALUES (10.5705,'2005-05-18 19:14:34');
INSERT INTO `cashbox` VALUES (10.57,'2005-05-18 19:17:23');
INSERT INTO `cashbox` VALUES (20.5805,'2005-05-18 19:18:10');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-29 12:43:11');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 13:33:12');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 13:34:42');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 13:40:22');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 13:41:24');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 13:46:10');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 13:53:29');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 13:59:19');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 14:07:30');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 14:10:20');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 14:14:43');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:14:20');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:15:15');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:16:10');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:16:57');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:17:03');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:27:49');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:28:37');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:29:20');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:32:46');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:33:57');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:34:29');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:35:55');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:37:54');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:38:41');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:40:16');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:40:21');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:41:03');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:43:39');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:45:34');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:49:51');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:52:33');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 15:55:04');
INSERT INTO `cashbox` VALUES (20.58,'2005-07-31 16:17:48');
INSERT INTO `cashbox` VALUES (20.58,'2005-08-03 14:37:07');

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `title_id` int(11) default NULL,
  `category_name` varchar(255) default NULL,
  `id` int(11) NOT NULL auto_increment,
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;

--
-- Dumping data for table `category`
--

INSERT INTO `category` VALUES (12,'Fiction - Science Fiction',5);
INSERT INTO `category` VALUES (12,'Science Fiction',6);
INSERT INTO `category` VALUES (12,'Science Fiction - Adventure',7);
INSERT INTO `category` VALUES (12,'Fiction / Science Fiction / Adventure',8);

--
-- Table structure for table `notes`
--

CREATE TABLE `notes` (
  `message` text,
  `author` varchar(32) default NULL,
  `whenEntered` datetime default NULL
) TYPE=MyISAM;

--
-- Dumping data for table `notes`
--


--
-- Table structure for table `title`
--

CREATE TABLE `title` (
  `id` int(11) NOT NULL auto_increment,
  `isbn` varchar(10) default NULL,
  `booktitle` text,
  `publisher` text,
  `release_date` varchar(255) default NULL,
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;

--
-- Dumping data for table `title`
--

INSERT INTO `title` VALUES (12,'0553572393','Green Mars (Mars Trilogy)','Spectra',NULL);

--
-- Table structure for table `transactionLog`
--

CREATE TABLE `transactionLog` (
  `action` varchar(255) default NULL,
  `amount` float default NULL,
  `date` datetime default NULL,
  `cashier` varchar(255) default NULL,
  `info` blob
) TYPE=MyISAM;

--
-- Dumping data for table `transactionLog`
--

INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',0,'2005-05-18 17:50:30',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',1,'2005-05-18 17:52:28','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',1,'2005-05-18 18:38:45',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',1,'2005-05-18 18:38:47','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',1,'2005-05-18 18:39:45',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',1,'2005-05-18 18:39:46','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',1,'2005-05-18 18:42:21',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',1,'2005-05-18 18:42:23','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',1,'2005-05-18 18:59:58',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',1,'2005-05-18 19:00:01','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',1,'2005-05-18 19:01:13',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',1,'2005-05-18 19:01:14','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',1,'2005-05-18 19:02:16',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',1,'2005-05-18 19:04:04','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',1,'2005-05-18 19:05:26',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',1,'2005-05-18 19:05:28','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',1,'2005-05-18 19:07:53',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',1,'2005-05-18 19:07:54','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',1,'2005-05-18 19:09:23',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',1,'2005-05-18 19:09:25','john',NULL);
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:09:44','john','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:09:44','john','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:09:44','john','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:09:44','john','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:09:44','john','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:09:44','john','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:09:44','john','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',-10,'2005-05-18 19:09:44','john','Discount 5.00');
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',1.5105,'2005-05-18 19:10:57',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',1.51,'2005-05-18 19:11:05','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',1.51,'2005-05-18 19:11:45',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',1.51,'2005-05-18 19:11:48','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',1.51,'2005-05-18 19:13:47',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',1.51,'2005-05-18 19:13:49','j',NULL);
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:14:32','j','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:14:32','j','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:14:32','j','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:14:32','j','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:14:32','j','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:14:32','j','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:14:32','j','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',-0.5005,'2005-05-18 19:14:32','j','5.00 % Discount');
INSERT INTO `transactionLog` VALUES ('SALE',-0.951,'2005-05-18 19:14:32','j','10.00 % Discount');
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',10.5705,'2005-05-18 19:17:22',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',10.57,'2005-05-18 19:17:23','j',NULL);
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:18:09','j','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:18:09','j','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:18:09','j','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:18:09','j','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:18:09','j','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:18:09','j','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',1.43,'2005-05-18 19:18:09','j','In House Coffee');
INSERT INTO `transactionLog` VALUES ('SALE',-0.5,'2005-05-18 19:18:09','j','5.00 % Discount');
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.5805,'2005-07-29 12:43:09',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-29 12:43:11','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 13:33:08',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 13:33:12','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 13:34:40',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 13:34:42','g',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 13:40:20',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 13:40:22','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 13:41:23',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 13:41:24','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 13:44:41',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 13:46:10','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 13:53:20',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 13:53:29','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 13:59:13',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 13:59:19','john',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 14:07:28',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 14:07:30','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 14:10:18',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 14:10:20','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 14:14:41',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 14:14:43','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:14:19',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:14:20','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:15:14',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:15:15','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:16:08',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:16:10','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:16:55',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:16:57','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:17:00',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:17:03','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:27:47',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:27:49','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:28:36',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:28:37','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:29:19',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:29:20','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:32:45',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:32:46','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:33:56',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:33:57','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:34:24',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:34:29','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:35:54',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:35:55','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:37:50',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:37:54','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:38:39',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:38:41','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:40:14',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:40:16','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:40:20',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:40:21','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:41:00',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:41:03','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:43:37',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:43:39','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:45:33',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:45:34','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:49:49',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:49:51','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:52:30',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:52:33','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 15:55:02',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 15:55:04','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-07-31 16:17:45',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-07-31 16:17:48','j',NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_PRECOUNT',20.58,'2005-08-03 14:37:04',NULL,NULL);
INSERT INTO `transactionLog` VALUES ('OPEN_POSTCOUNT',20.58,'2005-08-03 14:37:07','test',NULL);

