CREATE TABLE `users` (
  `user_id` INT PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(50) UNIQUE NOT NULL,
  `email` VARCHAR(100) UNIQUE NOT NULL,
  `password_hash` TEXT NOT NULL,
  `avatar_url` VARCHAR(255),
  `status` ENUM ('online', 'offline', 'away'),
  `last_seen` DATETIME,
  `created_at` TIMESTAMP DEFAULT (CURRENT_TIMESTAMP),
  `updated_at` TIMESTAMP DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `chats` (
  `chat_id` INT PRIMARY KEY AUTO_INCREMENT,
  `title` VARCHAR(100),
  `description` TEXT,
  `avatar_url` VARCHAR(255),
  `type` ENUM ('PRIVATE', 'GROUP', 'CHANNEL') NOT NULL,
  `is_public` BOOLEAN DEFAULT false,
  `owner_id` INT,
  `settings` JSON,
  `created_at` TIMESTAMP DEFAULT (CURRENT_TIMESTAMP),
  `updated_at` TIMESTAMP DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `chat_participants` (
  `participant_id` INT PRIMARY KEY AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `chat_id` INT NOT NULL,
  `role` ENUM ('OWNER', 'ADMIN', 'MEMBER') DEFAULT 'MEMBER',
  `joined_at` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `left_at` DATETIME DEFAULT null,
  `is_muted` BOOLEAN DEFAULT false
);

CREATE TABLE `messages` (
  `message_id` INT PRIMARY KEY AUTO_INCREMENT,
  `text` TEXT,
  `attachment_url` VARCHAR(255),
  `attachment_type` VARCHAR(50),
  `metadata` JSON,
  `is_edited` BOOLEAN DEFAULT false,
  `is_deleted` BOOLEAN DEFAULT false,
  `reply_to_id` INT DEFAULT null,
  `reactions` JSON,
  `delivered_to` JSON DEFAULT ('[]'),
  `read_by` JSON DEFAULT ('[]'),
  `chat_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `created_at` DATETIME DEFAULT (CURRENT_TIMESTAMP),
  `updated_at` DATETIME DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `asset_tokens` (
  `token_id` CHAR(36) PRIMARY KEY,
  `asset_url` VARCHAR(255) NOT NULL,
  `expires_at` DATETIME NOT NULL,
  `created_at` DATETIME DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `refresh_tokens` (
  `token_id` CHAR(36) PRIMARY KEY,
  `user_id` INT NOT NULL,
  `token` TEXT NOT NULL,
  `expires_at` DATETIME NOT NULL,
  `revoked` BOOLEAN DEFAULT false,
  `created_at` DATETIME DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `encryption_keys` (
  `key_id` INT PRIMARY KEY AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `public_key` TEXT NOT NULL,
  `private_key_encrypted` TEXT NOT NULL,
  `fingerprint` VARCHAR(64) NOT NULL,
  `created_at` DATETIME DEFAULT (CURRENT_TIMESTAMP)
);

CREATE INDEX `idx_chats_title` ON `chats` (`title`);

CREATE UNIQUE INDEX `chat_participants_index_1` ON `chat_participants` (`user_id`, `chat_id`);

CREATE INDEX `idx_messages_chatid_createdat` ON `messages` (`chat_id`, `created_at`);

ALTER TABLE `chats` ADD FOREIGN KEY (`owner_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `chat_participants` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `chat_participants` ADD FOREIGN KEY (`chat_id`) REFERENCES `chats` (`chat_id`);

ALTER TABLE `messages` ADD FOREIGN KEY (`chat_id`) REFERENCES `chats` (`chat_id`);

ALTER TABLE `messages` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `messages` ADD FOREIGN KEY (`reply_to_id`) REFERENCES `messages` (`message_id`);

ALTER TABLE `refresh_tokens` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

ALTER TABLE `encryption_keys` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
