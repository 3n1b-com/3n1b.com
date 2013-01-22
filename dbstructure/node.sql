-- ----------------------------
--  Table structure for `node`
-- ----------------------------
DROP TABLE IF EXISTS `node`;
CREATE TABLE `node` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text,
  `slug` text,
  `thumb` text,
  `introduction` text,
  `created` text,
  `updated` text,
  `plane_id` int(11) DEFAULT NULL,
  `topic_count` int(11) DEFAULT NULL,
  `custom_style` text,
  `limit_reputation` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;

INSERT INTO `node` VALUES (1,'Test', 'test', '', 'Just test', '2013-01-22', '2013-01-22', 1, 0, '', 10000);
INSERT INTO `node` VALUES (2,'搞笑', 'fun', '', '各种搞笑', '2013-01-22', '2013-01-22', 1, 0, '', 10000);
INSERT INTO `node` VALUES (3,'电影', 'movie', '', '分享好看电影', '2013-01-22', '2013-01-22', 1, 0, '', 10000);
INSERT INTO `node` VALUES (4,'音乐', 'music', '', '倾听', '2013-01-22', '2013-01-22', 1, 0, '', 10000);
INSERT INTO `node` VALUES (5,'程序员', 'coder', '', '程序猿', '2013-01-22', '2013-01-22', 1, 0, '', 10000);
INSERT INTO `node` VALUES (6,'NBA', 'nba', '', 'NBA', '2013-01-22', '2013-01-22', 1, 0, '', 10000);