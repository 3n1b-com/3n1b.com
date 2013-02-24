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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- 分享 --
INSERT INTO `node` VALUES (1,'问与答', 'qna', '', '', '2013-01-22', '2013-01-22', 1, 0, '', 10000);
INSERT INTO `node` VALUES (2,'分享发现', 'share', '', '', '2013-01-22', '2013-01-22', 1, 0, '', 10000); 
INSERT INTO `node` VALUES (3,'自言自语', 'autistic', '', '', '2013-01-22', '2013-01-22', 1, 0, '', 10000);
INSERT INTO `node` VALUES (4,'随想', 'random', '', '', '2013-01-22', '2013-01-22', 1, 0, '', 10000);
INSERT INTO `node` VALUES (5,'奇思妙想', 'ideas', '', '', '2013-01-22', '2013-01-22', 1, 0, '', 10000);
INSERT INTO `node` VALUES (49,'Top10', 'top10', '', '', '2013-01-22', '2013-01-22', 1, 0, '', 10000);
-- 生活 --
INSERT INTO `node` VALUES (6,'团购分享', 'tuan', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (7,'阅读', 'reading', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (8,'征友', 'date', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (9,'跳蚤市场', 'second', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (10,'摄影', 'photograph', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (11,'骑行', 'bike', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (12,'驴友', 'travel', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (13,'绿茵场', 'soccer', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (54,'DIY', 'DIY', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
INSERT INTO `node` VALUES (55,'文艺', 'literary', '', '', '2013-01-22', '2013-01-22', 2, 0, '', 10000);
-- 娱乐 --
INSERT INTO `node` VALUES (14,'搞笑', 'fun', '', '各种搞笑', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (15,'电影', 'movie', '', '分享好看电影', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (16,'音乐', 'music', '', '倾听', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (17,'游戏', 'games', '', '', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (18,'DOTA', 'dota', '', '', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (19,'动漫', 'anime', '', '', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (20,'TV', 'tv', '', '', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (51,'手机', 'phone', '', '', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (52,'平板', 'pad', '', '', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (53,'数码控', 'digital', '', '', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
INSERT INTO `node` VALUES (56,'萌', 'cute', '', '', '2013-01-22', '2013-01-22', 3, 0, '', 10000);
-- 学习 --
INSERT INTO `node` VALUES (21,'编程', 'programming', '', '', '2013-01-22', '2013-01-22', 4, 0, '', 10000);
INSERT INTO `node` VALUES (22,'托福', 'toefl', '', '', '2013-01-22', '2013-01-22', 4, 0, '', 10000);
INSERT INTO `node` VALUES (23,'GRE', 'GRE', '', '', '2013-01-22', '2013-01-22', 4, 0, '', 10000);
INSERT INTO `node` VALUES (24,'考研', 'master', '', '', '2013-01-22', '2013-01-22', 4, 0, '', 10000);
INSERT INTO `node` VALUES (25,'历史', 'history', '', '', '2013-01-22', '2013-01-22', 4, 0, '', 10000);
INSERT INTO `node` VALUES (26,'文学', 'literature', '', '', '2013-01-22', '2013-01-22', 4, 0, '', 10000);
INSERT INTO `node` VALUES (27,'设计', 'design', '', '', '2013-01-22', '2013-01-22', 4, 0, '', 10000);
INSERT INTO `node` VALUES (28,'国学', 'chinese', '', '', '2013-01-22', '2013-01-22', 4, 0, '', 10000);
INSERT INTO `node` VALUES (29,'艺术', 'art', '', '', '2013-01-22', '2013-01-22', 4, 0, '', 10000);
-- 工作 --
INSERT INTO `node` VALUES (30,'程序员', 'coder', '', '程序猿', '2013-01-22', '2013-01-22', 4, 0, '', 10000);
INSERT INTO `node` VALUES (31,'酷工作', 'jobs', '', '', '2013-01-22', '2013-01-22', 5, 0, '', 10000);
INSERT INTO `node` VALUES (32,'兼职', 'parttime', '', '', '2013-01-22', '2013-01-22', 5, 0, '', 10000);
INSERT INTO `node` VALUES (33,'研究所', 'research', '', '', '2013-01-22', '2013-01-22', 5, 0, '', 10000);
INSERT INTO `node` VALUES (34,'面经', 'interview', '', '', '2013-01-22', '2013-01-22', 5, 0, '', 10000);
INSERT INTO `node` VALUES (35,'职场', 'career', '', '', '2013-01-22', '2013-01-22', 5, 0, '', 10000);
INSERT INTO `node` VALUES (36,'内部推荐', 'recommendation', '', '', '2013-01-22', '2013-01-22', 5, 0, '', 10000);
INSERT INTO `node` VALUES (50,'创业', 'startup', '', '', '2013-01-22', '2013-01-22', 5, 0, '', 10000);
-- 城市 --
INSERT INTO `node` VALUES (37,'北京', 'beijing', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
INSERT INTO `node` VALUES (38,'上海', 'shanghai', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
INSERT INTO `node` VALUES (39,'南京', 'nanjing', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
INSERT INTO `node` VALUES (40,'西安', 'xian', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
INSERT INTO `node` VALUES (41,'杭州', 'hangzhou', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
INSERT INTO `node` VALUES (42,'武汉', 'wuhan', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
INSERT INTO `node` VALUES (43,'深圳', 'shenzhen', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
INSERT INTO `node` VALUES (44,'广州', 'guangzhou', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
INSERT INTO `node` VALUES (45,'成都', 'chendu', '', '', '2013-01-22', '2013-01-22', 6, 0, '', 10000);
-- 社区 --
INSERT INTO `node` VALUES (46,'公告通知', 'placard', '', 'Just test', '2013-01-22', '2013-01-22', 7, 0, '', 10000);
INSERT INTO `node` VALUES (47,'反馈建议', 'feedback', '', '', '2013-01-22', '2013-01-22', 7, 0, '', 10000);
INSERT INTO `node` VALUES (48,'使用指南', 'guide', '', '', '2013-01-22', '2013-01-22', 7, 0, '', 10000);                     