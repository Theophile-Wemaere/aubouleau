CREATE TABLE `users` (
  `id` int AUTO_INCREMENT PRIMARY KEY,
  `first_name` varchar(255),
  `last_name` varchar(255),
  `email` varchar(255),
  `password` text,
  `role` integer,
  `created_at` timestamp
);

CREATE TABLE `problems` (
  `id` int AUTO_INCREMENT PRIMARY KEY,
  `status` varchar(255),
  `title` varchar(255),
  `description` text,
  `room` int,
  `equipment` int,
  `reporter` int,
  `solver` int
);

CREATE TABLE `rooms` (
  `id` int AUTO_INCREMENT PRIMARY KEY,
  `number` varchar(255),
  `name` varchar(255),
  `floor` varchar(255)
);

CREATE TABLE `time_slot` (
  `id` int AUTO_INCREMENT PRIMARY KEY,
  `subject` varchar(255),
  `start` datetime,
  `end` datetime,
  `room` int
);

CREATE TABLE `floor` (
  `id` varchar(255) PRIMARY KEY,
  `number` int,
  `name` text,
  `building` int
);

CREATE TABLE `building` (
  `id` int AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(255)
);

CREATE TABLE `equipments` (
  `id` int AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(255),
  `room` int,
  `type` int
);

CREATE TABLE `equipment_type` (
  `id` int AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(255),
  `manufacturer` varchar(255),
  `model` varchar(255)
);

ALTER TABLE `floor` ADD FOREIGN KEY (`building`) REFERENCES `building` (`id`);

ALTER TABLE `rooms` ADD FOREIGN KEY (`floor`) REFERENCES `floor` (`id`);

ALTER TABLE `time_slot` ADD FOREIGN KEY (`room`) REFERENCES `rooms` (`id`);

ALTER TABLE `problems` ADD FOREIGN KEY (`room`) REFERENCES `rooms` (`id`);

ALTER TABLE `problems` ADD FOREIGN KEY (`equipment`) REFERENCES `equipments` (`id`);

ALTER TABLE `problems` ADD FOREIGN KEY (`reporter`) REFERENCES `users` (`id`);

ALTER TABLE `problems` ADD FOREIGN KEY (`solver`) REFERENCES `users` (`id`);

ALTER TABLE `equipments` ADD FOREIGN KEY (`type`) REFERENCES `equipment_type` (`id`);

ALTER TABLE `equipments` ADD FOREIGN KEY (`room`) REFERENCES `rooms` (`id`);
