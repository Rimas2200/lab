-- Клиенты
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

-- Типы металлов
CREATE TABLE `metal_types` (
  `metal_type_id` INT PRIMARY KEY AUTO_INCREMENT,
  `type_name` VARCHAR(50) NOT NULL UNIQUE
);

-- Типы вставок
CREATE TABLE `inlay_types` (
  `inlay_type_id` INT PRIMARY KEY AUTO_INCREMENT,
  `type_name` VARCHAR(50) NOT NULL UNIQUE
);

-- Ценности
CREATE TABLE `valuables` (
  `valuable_id` INT PRIMARY KEY AUTO_INCREMENT,
  `client_id` INT,
  `metal_type_id` INT,
  `inlay_type_id` INT,
  `weight` DECIMAL(10,3),
  `purity` DECIMAL(5,2),
  `description` TEXT,
  `appraised_value` DECIMAL(15,2),
  `received_date` DATE,
  `storage_location` VARCHAR(100)
);

-- Ломбарды
CREATE TABLE `pawnshops` (
  `pawnshop_id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(100),
  `address` VARCHAR(255),
  `phone` VARCHAR(20),
  `email` VARCHAR(100),
  `working_hours` VARCHAR(50),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Сотрудники
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

-- Залоги
CREATE TABLE `pledges` (
  `pledge_id` INT PRIMARY KEY AUTO_INCREMENT,
  `valuable_id` INT,
  `pawnshop_id` INT,
  `employee_id` INT,
  `pledge_date` DATE,
  `end_date` DATE,
  `loan_amount` DECIMAL(15,2),
  `interest_rate` DECIMAL(5,2),
  `status` ENUM ('Активный', 'Выкуплен', 'Продан') DEFAULT 'Активный',
  `comments` TEXT
);

-- Платежи
CREATE TABLE `payments` (
  `payment_id` INT PRIMARY KEY AUTO_INCREMENT,
  `pledge_id` INT,
  `employee_id` INT,
  `payment_date` DATE,
  `amount` DECIMAL(15,2),
  `payment_type` ENUM ('Частичная выплата', 'Полный выкуп'),
  `comments` TEXT
);

-- Внешние ключи
ALTER TABLE `valuables` ADD FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`);
ALTER TABLE `valuables` ADD FOREIGN KEY (`metal_type_id`) REFERENCES `metal_types` (`metal_type_id`);
ALTER TABLE `valuables` ADD FOREIGN KEY (`inlay_type_id`) REFERENCES `inlay_types` (`inlay_type_id`);

ALTER TABLE `employees` ADD FOREIGN KEY (`pawnshop_id`) REFERENCES `pawnshops` (`pawnshop_id`);

ALTER TABLE `pledges` ADD FOREIGN KEY (`valuable_id`) REFERENCES `valuables` (`valuable_id`);
ALTER TABLE `pledges` ADD FOREIGN KEY (`pawnshop_id`) REFERENCES `pawnshops` (`pawnshop_id`);
ALTER TABLE `pledges` ADD FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`);

ALTER TABLE `payments` ADD FOREIGN KEY (`pledge_id`) REFERENCES `pledges` (`pledge_id`);
ALTER TABLE `payments` ADD FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`);

-- Триггер для обновления статуса залога после оплаты
DELIMITER //
CREATE TRIGGER after_payment_insert
AFTER INSERT ON payments
FOR EACH ROW
BEGIN
    DECLARE total_paid DECIMAL(15,2);
    
    -- Вычисляем общую сумму платежей по pledge_id
    SELECT SUM(amount) INTO total_paid
    FROM payments
    WHERE pledge_id = NEW.pledge_id;

    -- Получаем сумму кредита
    SELECT loan_amount INTO @loan_amount
    FROM pledges
    WHERE pledge_id = NEW.pledge_id;

    -- Обновляем статус, если сумма покрывает кредит
    IF total_paid >= @loan_amount THEN
        UPDATE pledges
        SET status = 'Выкуплен'
        WHERE pledge_id = NEW.pledge_id;
    ELSE
        UPDATE pledges
        SET status = 'Активный'
        WHERE pledge_id = NEW.pledge_id AND status != 'Продан';
    END IF;
END//
DELIMITER ;