CREATE TABLE `electricity_total_cost` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `log_date` date DEFAULT NULL,                          -- The billing date
  `total_morning_diff` decimal(15,2) DEFAULT NULL,       -- Sum of morning consumption
  `total_night_diff` decimal(15,2) DEFAULT NULL,         -- Sum of night consumption
  `day_cost` decimal(20,2) DEFAULT 0.00,                 -- Total cost for morning period
  `night_cost` decimal(20,2) DEFAULT 0.00,               -- Total cost for night period
  `total_cost` decimal(15,2) DEFAULT NULL,               -- Final total cost (Day + Night)
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;