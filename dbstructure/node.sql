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

INSERT INTO `node` VALUES (1,'公告通知', 'placard', '', 'Just test', '2013-01-22', '2013-01-22', 7, 0, '', 10000);
INSERT INTO `node` VALUES (2,'搞笑', 'fun', '', '各种搞笑', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (3,'电影', 'movie', '', '分享好看电影', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (4,'音乐', 'music', '', '倾听', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (5,'程序员', 'coder', '', '程序猿', '2013-01-22', '2013-01-22', 4, 0, '', 10000);
INSERT INTO `node` VALUES (6,'问与答', 'qna', '', '', '2013-01-22', '2013-01-22', 1, 0, '', 10000);
INSERT INTO `node` VALUES (7,'阅读', 'reading', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (8,'自言自语', 'autistic', '', '', '2013-01-22', '2013-01-22', 1, 0, '', 10000);
INSERT INTO `node` VALUES (9,'随想', 'random', '', '', '2013-01-22', '2013-01-22', 1, 0, '', 10000);
INSERT INTO `node` VALUES (10,'奇思妙想', 'ideas', '', '', '2013-01-22', '2013-01-22', 1, 0, '', 10000);
INSERT INTO `node` VALUES (11,'反馈建议', 'feedback', '', '', '2013-01-22', '2013-01-22', 7, 0, '', 10000);
INSERT INTO `node` VALUES (12,'使用指南', 'guide', '', '', '2013-01-22', '2013-01-22', 7, 0, '', 10000);
INSERT INTO `node` VALUES (13,'编程', 'programming', '', '', '2013-01-22', '2013-01-22', 4, 0, '', 10000);
INSERT INTO `node` VALUES (14,'游戏', 'games', '', '', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (15,'DOTA', 'dota', '', '', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (16,'英雄联盟', 'lol', '', '', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (17,'Xbox 360', 'xbox360', '', '', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (18,'PlayStation 3', 'ps3', '', '', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (19,'Google', 'google', '', '', '2013-01-22', '2013-01-22', 1, 0, '', 10000);
INSERT INTO `node` VALUES (20,'Apple', 'apple', '', '', '2013-01-22', '2013-01-22', 1, 0, '', 10000);
INSERT INTO `node` VALUES (21,'iPhone', 'iphone', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (22,'Mac', 'mac', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (23,'跳蚤市场', 'second', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (24,'酷工作', 'jobs', '', '', '2013-01-22', '2013-01-22', 5, 0, '', 10000);
INSERT INTO `node` VALUES (25,'兼职', 'parttime', '', '', '2013-01-22', '2013-01-22', 5, 0, '', 10000);
INSERT INTO `node` VALUES (26,'摄影', 'photograph', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (27,'团购分享', 'tuan', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (28,'骑行', 'bike', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (29,'驴友', 'travel', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (30,'绿茵场', 'soccer', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (31,'北京', 'beijing', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
INSERT INTO `node` VALUES (32,'上海', 'shanghai', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
INSERT INTO `node` VALUES (33,'南京', 'nanjing', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
INSERT INTO `node` VALUES (34,'西安', 'xian', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
INSERT INTO `node` VALUES (35,'杭州', 'hangzhou', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
INSERT INTO `node` VALUES (36,'武汉', 'wuhan', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
INSERT INTO `node` VALUES (37,'深圳', 'shenzhen', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
INSERT INTO `node` VALUES (38,'广州', 'guangzhou', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
INSERT INTO `node` VALUES (39,'成都', 'chendu', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
INSERT INTO `node` VALUES (40,'研究所', 'research', '', '', '2013-01-22', '2013-01-22', 5, 0, '', 10000);
INSERT INTO `node` VALUES (41,'面经', 'interview', '', '', '2013-01-22', '2013-01-22', 5, 0, '', 10000);
INSERT INTO `node` VALUES (42,'职场', 'career', '', '', '2013-01-22', '2013-01-22', 5, 0, '', 10000);
INSERT INTO `node` VALUES (43,'内部推荐', 'recommendation', '', '', '2013-01-22', '2013-01-22', 5, 0, '', 10000);
INSERT INTO `node` VALUES (44,'托福', 'toefl', '', '', '2013-01-22', '2013-01-22', 4, 0, '', 10000);
INSERT INTO `node` VALUES (45,'GRE', 'GRE', '', '', '2013-01-22', '2013-01-22', 4, 0, '', 10000);
INSERT INTO `node` VALUES (46,'考研', 'master', '', '', '2013-01-22', '2013-01-22', 4, 0, '', 10000);
INSERT INTO `node` VALUES (47,'历史', 'history', '', '', '2013-01-22', '2013-01-22', 4, 0, '', 10000);
INSERT INTO `node` VALUES (48,'文学', 'literature', '', '', '2013-01-22', '2013-01-22', 4, 0, '', 10000);
INSERT INTO `node` VALUES (49,'设计', 'design', '', '', '2013-01-22', '2013-01-22', 4, 0, '', 10000);                             