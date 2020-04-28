CREATE DATABASE IF NOT EXISTS Monologue;
USE Monologue;
CREATE TABLE IF NOT EXISTS `Logue` (
    `id` int unsigned NOT NULL AUTO_INCREMENT,
    `title` varchar(50) NOT NULL,
    `contents` text NOT NULL,
    `type` varchar(10) NOT NULL,
    `date` varchar(20) NOT NULL,
    PRIMARY KEY (`id`)
) CHARSET=utf8mb4;
CREATE TABLE IF NOT EXISTS `User` (
    `id` int unsigned NOT NULL AUTO_INCREMENT,
    `username` varchar(20) NOT NULL,
    `password` varchar(512) NOT NULL,
    PRIMARY KEY (`id`)
) CHARSET=utf8mb4;