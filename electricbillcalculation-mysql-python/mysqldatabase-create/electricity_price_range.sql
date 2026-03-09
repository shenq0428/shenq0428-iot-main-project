CREATE TABLE `electricity_price_range` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `day_type` int(11) NOT NULL,                           -- Day category ID
  `start_time` time DEFAULT NULL,                        -- Period start (e.g., 08:00:01)
  `end_time` time DEFAULT NULL,                          -- Period end (e.g., 20:00:00)
  `price` decimal(10,2) DEFAULT NULL,                    -- Rate per kWh
  `description` varchar(20) DEFAULT NULL,                -- 'morning' or 'night'
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 清空旧数据并重新插入最新的费率配置
TRUNCATE TABLE electricity_price_range;

INSERT INTO electricity_price_range (day_type, start_time, end_time, price, description) VALUES
(1, '08:00:01', '20:00:00', 0.50, 'morning'), -- 白天时段
(1, '20:00:01', '23:59:59', 0.30, 'night'),   -- 夜间时段 A
(2, '00:00:00', '08:00:00', 0.30, 'night');   -- 夜间时段 B (统一分类)
