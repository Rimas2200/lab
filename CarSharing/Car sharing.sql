CREATE TABLE `users` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `email` VARCHAR(255) UNIQUE NOT NULL,
  `phone` VARCHAR(20),
  `first_name` VARCHAR(100),
  `last_name` VARCHAR(100),
  `password_hash` TEXT NOT NULL,
  `license_number` VARCHAR(50),
  `created_at` TIMESTAMP DEFAULT (CURRENT_TIMESTAMP),
  `is_blocked` BOOLEAN DEFAULT false
);

CREATE TABLE `cars` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `vin` VARCHAR(17) UNIQUE NOT NULL,
  `brand` VARCHAR(50),
  `model` VARCHAR(50),
  `year` SMALLINT,
  `color` VARCHAR(30),
  `license_plate` VARCHAR(20) UNIQUE NOT NULL,
  `current_location_id` INT,
  `status` ENUM ('available', 'rented', 'maintenance') DEFAULT 'available',
  `hourly_rate` DECIMAL(10,2),
  `daily_rate` DECIMAL(10,2),
  `available_for_rent` BOOLEAN DEFAULT true
);

CREATE TABLE `locations` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(100),
  `address` TEXT,
  `latitude` DECIMAL(9,6),
  `longitude` DECIMAL(9,6)
);

CREATE TABLE `bookings` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `car_id` INT NOT NULL,
  `start_time` TIMESTAMP NOT NULL,
  `end_time` TIMESTAMP NOT NULL,
  `status` ENUM ('active', 'canceled', 'completed') DEFAULT 'active',
  `created_at` TIMESTAMP DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `trips` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `booking_id` INT NOT NULL,
  `end_location_id` INT,
  `start_location_id` INT NOT NULL,
  `start_time` TIMESTAMP NOT NULL,
  `end_time` TIMESTAMP,
  `total_minutes` INT,
  `distance_km` DECIMAL(10,2),
  `cost` DECIMAL(10,2),
  `status` ENUM ('started', 'finished', 'interrupted') DEFAULT 'started'
);

CREATE TABLE `payments` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `trip_id` INT NOT NULL,
  `amount` DECIMAL(10,2) NOT NULL,
  `payment_method` VARCHAR(50),
  `status` ENUM ('success', 'failed', 'pending') DEFAULT 'pending',
  `created_at` TIMESTAMP DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `tariffs` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `rate_type` ENUM ('hourly', 'daily', 'weekly') NOT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `description` TEXT
);

CREATE TABLE `car_locations_history` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `car_id` INT NOT NULL,
  `location_id` INT NOT NULL,
  `timestamp` TIMESTAMP DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `reviews` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `trip_id` INT NOT NULL,
  `rating` SMALLINT,
  `comment` TEXT,
  `created_at` TIMESTAMP DEFAULT (CURRENT_TIMESTAMP)
);

ALTER TABLE `cars` ADD FOREIGN KEY (`current_location_id`) REFERENCES `locations` (`id`);

ALTER TABLE `bookings` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `bookings` ADD FOREIGN KEY (`car_id`) REFERENCES `cars` (`id`);

ALTER TABLE `trips` ADD FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`);

ALTER TABLE `trips` ADD FOREIGN KEY (`start_location_id`) REFERENCES `locations` (`id`);

ALTER TABLE `trips` ADD FOREIGN KEY (`end_location_id`) REFERENCES `locations` (`id`);

ALTER TABLE `payments` ADD FOREIGN KEY (`trip_id`) REFERENCES `trips` (`id`);

ALTER TABLE `car_locations_history` ADD FOREIGN KEY (`car_id`) REFERENCES `cars` (`id`);

ALTER TABLE `car_locations_history` ADD FOREIGN KEY (`location_id`) REFERENCES `locations` (`id`);

ALTER TABLE `reviews` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `reviews` ADD FOREIGN KEY (`trip_id`) REFERENCES `trips` (`id`);

ALTER TABLE `trips` ADD FOREIGN KEY (`start_location_id`) REFERENCES `trips` (`end_location_id`);
