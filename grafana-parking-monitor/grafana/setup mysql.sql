CREATE TABLE parking_sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    floor INT,               -- 1, 2, or 3
    space_id INT,            -- 1 to 10
    status INT,              -- 0: Available, 1: Occupied
    battery_level INT        -- 0 to 100
);