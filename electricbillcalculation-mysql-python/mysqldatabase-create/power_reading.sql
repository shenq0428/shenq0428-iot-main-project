CREATE TABLE `power_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NULL DEFAULT current_timestamp(), -- Date and time of the reading
  `val` int(11) DEFAULT NULL,                            -- Total cumulative kWh
  `increment` int(11) DEFAULT NULL,                      -- Auto-calculated increment (optional)
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;