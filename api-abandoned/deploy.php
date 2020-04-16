<?php

$db = new mysqli("localhost", "root", "subilan1999");

$db->query("CREATE DATABASE Monologue");
$db->query("USE Monologue");
$db->query("SET NAMES=utf8");

$db->query("CREATE TABLE Logue (
    `id` INT UNSIGNED AUTO_INCREMENT,
    `title` VARCHAR(50) NOT NULL,
    `contents` TEXT NOT NULL,
    `date` VARCHAR(15) NOT NULL,
    `extdate` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`id`)
) CHARACTER SET=utf8mb4");

$db->query("CREATE TABLE User (
    `id` INT UNSIGNED AUTO_INCREMENT,
    `username` VARCHAR(20) NOT NULL,
    `password` VARCHAR(512) NOT NULL,
    PRIMARY KEY (`id`)
)");

$username = "admin";
$password = password_hash("subilan1999", PASSWORD_DEFAULT);

$db->query("INSERT INTO User (username, password)
VALUES ('$username', '$password')");

if (empty($db->error)) {
    echo "Done";
} else {
    echo $db->error;
}