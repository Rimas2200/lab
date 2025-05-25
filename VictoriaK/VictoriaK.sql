CREATE TABLE `clients` (
  `client_id` INT PRIMARY KEY AUTO_INCREMENT,
  `surname` VARCHAR(50),
  `name` VARCHAR(50),
  `patronymic` VARCHAR(50),
  `birth_date` DATE,
  `passport_series` VARCHAR(10),
  `passport_number` VARCHAR(20),
  `passport_issued_by` VARCHAR(255),
  `passport_issue_date` DATE,
  `residence_address` VARCHAR(255),         -- Адрес проживания
  `registration_address` VARCHAR(255),      -- Адрес регистрации
  `phone` INT(10),                          -- Телефон как INT(10)
  `email` VARCHAR(100),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `car_brands` (
  `brand_id` INT PRIMARY KEY AUTO_INCREMENT,
  `brand_name` VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE `cars` (
  `car_id` INT PRIMARY KEY AUTO_INCREMENT,
  `client_id` INT,
  `brand_id` INT,                           -- Ссылка на марку из car_brands
  `model` VARCHAR(50),
  `year` INT,
  `vin` VARCHAR(17) UNIQUE,
  `license_plate` VARCHAR(15),
  `technical_passport` VARCHAR(50),
  `color` VARCHAR(30),
  `engine_capacity` DECIMAL(5,2),
  `fuel_type` ENUM ('Бензин', 'Дизель', 'Электро', 'Гибрид'),
  `mileage` INT
);

CREATE TABLE `pawnshops` (
  `pawnshop_id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(100),
  `address` VARCHAR(255),
  `phone` VARCHAR(20),
  `email` VARCHAR(100),
  `working_hours` VARCHAR(50),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `employees` (
  `employee_id` INT PRIMARY KEY AUTO_INCREMENT,
  `pawnshop_id` INT,
  `surname` VARCHAR(50),
  `name` VARCHAR(50),
  `patronymic` VARCHAR(50),
  `position` VARCHAR(50),
  `phone` VARCHAR(20),
  `email` VARCHAR(100),
  `hire_date` DATE
);

CREATE TABLE `pledges` (
  `pledge_id` INT PRIMARY KEY AUTO_INCREMENT,
  `car_id` INT,
  `pawnshop_id` INT,
  `employee_id` INT,
  `pledge_date` DATE,
  `end_date` DATE,
  `amount` DECIMAL(15,2),
  `interest_rate` DECIMAL(5,2),
  `status` ENUM ('Активный', 'Выкуплен', 'Продан') DEFAULT 'Активный',
  `comments` TEXT
);

CREATE TABLE `payments` (
  `payment_id` INT PRIMARY KEY AUTO_INCREMENT,
  `pledge_id` INT,
  `employee_id` INT,
  `payment_date` DATE,
  `amount` DECIMAL(15,2),
  `payment_type` ENUM ('Частичная выплата', 'Полный выкуп'),
  `comments` TEXT
);

-- car_photos

-- Внешние ключи

ALTER TABLE `cars` ADD FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`);
ALTER TABLE `cars` ADD FOREIGN KEY (`brand_id`) REFERENCES `car_brands` (`brand_id`);

ALTER TABLE `employees` ADD FOREIGN KEY (`pawnshop_id`) REFERENCES `pawnshops` (`pawnshop_id`);

ALTER TABLE `pledges` ADD FOREIGN KEY (`car_id`) REFERENCES `cars` (`car_id`);
ALTER TABLE `pledges` ADD FOREIGN KEY (`pawnshop_id`) REFERENCES `pawnshops` (`pawnshop_id`);
ALTER TABLE `pledges` ADD FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`);

ALTER TABLE `payments` ADD FOREIGN KEY (`pledge_id`) REFERENCES `pledges` (`pledge_id`);
ALTER TABLE `payments` ADD FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`);

ALTER TABLE `sold_cars` ADD FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`);
ALTER TABLE `sold_cars` ADD FOREIGN KEY (`car_id`) REFERENCES `cars` (`car_id`);

ALTER TABLE `redeemed_cars` ADD FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`);
ALTER TABLE `redeemed_cars` ADD FOREIGN KEY (`car_id`) REFERENCES `cars` (`car_id`);

-- Таблицы sold_cars и redeemed_cars остаются без изменений

CREATE TABLE `sold_cars` (
  `sold_id` INT PRIMARY KEY AUTO_INCREMENT,
  `client_id` INT,
  `car_id` INT,
  `pledge_amount` DECIMAL(15,2),
  `sold_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `redeemed_cars` (
  `redeemed_id` INT PRIMARY KEY AUTO_INCREMENT,
  `client_id` INT,
  `car_id` INT,
  `pledge_amount` DECIMAL(15,2),
  `redeemed_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$

-- Триггер на добавление записи в sold_cars при статусе "Продан"
CREATE TRIGGER after_pledge_status_update_sold
AFTER UPDATE ON pledges
FOR EACH ROW
BEGIN
  IF NEW.status = 'Продан' AND OLD.status != 'Продан' THEN
    INSERT INTO sold_cars (client_id, car_id, pledge_amount)
    VALUES (
      (SELECT client_id FROM cars WHERE car_id = NEW.car_id),
      NEW.car_id,
      NEW.amount
    );
  END IF;
END$$

-- Триггер на добавление записи в redeemed_cars при статусе "Выкуплен"
CREATE TRIGGER after_pledge_status_update_redeemed
AFTER UPDATE ON pledges
FOR EACH ROW
BEGIN
  IF NEW.status = 'Выкуплен' AND OLD.status != 'Выкуплен' THEN
    INSERT INTO redeemed_cars (client_id, car_id, pledge_amount)
    VALUES (
      (SELECT client_id FROM cars WHERE car_id = NEW.car_id),
      NEW.car_id,
      NEW.amount
    );
  END IF;
END$$

DELIMITER ;