# MySQL-Front 3.2  (Build 14.8)

/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='SYSTEM' */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE */;
/*!40101 SET SQL_MODE='STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES */;
/*!40103 SET SQL_NOTES='ON' */;


# Host: localhost    Database: redekuai_development
# ------------------------------------------------------
# Server version 5.0.18-nt

/*!40101 SET NAMES utf8 */;

#
# Table structure for table province
#

CREATE TABLE `province` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(11) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

#
# Dumping data for table province
#

INSERT INTO `province` VALUES (1,'北京');
INSERT INTO `province` VALUES (2,'上海');
INSERT INTO `province` VALUES (3,'天津');
INSERT INTO `province` VALUES (4,'重庆');
INSERT INTO `province` VALUES (5,'黑龙江');
INSERT INTO `province` VALUES (6,'吉林');
INSERT INTO `province` VALUES (7,'辽宁');
INSERT INTO `province` VALUES (8,'山东');
INSERT INTO `province` VALUES (9,'山西');
INSERT INTO `province` VALUES (10,'陕西');
INSERT INTO `province` VALUES (11,'河北');
INSERT INTO `province` VALUES (12,'河南');
INSERT INTO `province` VALUES (13,'湖北');
INSERT INTO `province` VALUES (14,'湖南');
INSERT INTO `province` VALUES (15,'海南');
INSERT INTO `province` VALUES (16,'江苏');
INSERT INTO `province` VALUES (17,'江西');
INSERT INTO `province` VALUES (18,'广东');
INSERT INTO `province` VALUES (19,'广西');
INSERT INTO `province` VALUES (20,'云南');
INSERT INTO `province` VALUES (21,'贵州');
INSERT INTO `province` VALUES (22,'四川');
INSERT INTO `province` VALUES (23,'内蒙古');
INSERT INTO `province` VALUES (24,'宁夏');
INSERT INTO `province` VALUES (25,'甘肃');
INSERT INTO `province` VALUES (26,'青海');
INSERT INTO `province` VALUES (27,'西藏');
INSERT INTO `province` VALUES (28,'新疆');
INSERT INTO `province` VALUES (29,'安徽');
INSERT INTO `province` VALUES (30,'浙江');
INSERT INTO `province` VALUES (31,'福建');
INSERT INTO `province` VALUES (32,'台湾');
INSERT INTO `province` VALUES (33,'香港');
INSERT INTO `province` VALUES (34,'澳门');
INSERT INTO `province` VALUES (35,'国外');

/*!40101 SET NAMES latin1 */;

/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
