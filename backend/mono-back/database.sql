CREATE DATABASE Monologue;
USE Monologue;
CREATE TABLE `Logue` (
    `id` int unsigned NOT NULL AUTO_INCREMENT,
    `title` varchar(50) NOT NULL,
    `contents` text NOT NULL,
    `date` varchar(15) NOT NULL,
    `extdate` varchar(45) NOT NULL,
    PRIMARY KEY (`id`)
) CHARSET=utf8mb4;
CREATE TABLE `User` (
    `id` int unsigned NOT NULL AUTO_INCREMENT,
    `username` varchar(20) NOT NULL,
    `password` varchar(512) NOT NULL,
    PRIMARY KEY (`id`)
) CHARSET=utf8mb4;