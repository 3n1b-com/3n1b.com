-- ----------------------------
--  Table structure for `plane`
-- ----------------------------
DROP TABLE IF EXISTS `plane`;
CREATE TABLE `plane` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text,
  `created` text,
  `updated` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO `plane` VALUES (1,'分 享', '2013-01-23', '2013-01-23');
INSERT INTO `plane` VALUES (2,'生 活', '2013-01-23', '2013-01-23');
INSERT INTO `plane` VALUES (3,'娱 乐', '2013-01-23', '2013-01-23');
INSERT INTO `plane` VALUES (4,'学 习', '2013-01-23', '2013-01-23');
INSERT INTO `plane` VALUES (5,'工 作', '2013-01-23', '2013-01-23');
INSERT INTO `plane` VALUES (6,'城 市', '2013-01-23', '2013-01-23');
INSERT INTO `plane` VALUES (7,'社 区', '2013-01-23', '2013-01-23');