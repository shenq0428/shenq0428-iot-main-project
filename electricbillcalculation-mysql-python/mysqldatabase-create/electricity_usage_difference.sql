CREATE TABLE `electricity_usage_difference` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `window_end_time` datetime DEFAULT NULL,                -- End of the calculation window
  `net_diff` bigint(20) DEFAULT NULL,                     -- The actual kWh consumed (current - previous)
  `morning_night` varchar(20) DEFAULT NULL,               -- Categorized period (Morning/Night)
  PRIMARY KEY (`id`),
  -- 关键修复：添加唯一索引 --
  UNIQUE KEY `unique_window` (`window_end_time`)          
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;