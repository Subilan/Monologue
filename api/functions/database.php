<?php

class db {
    private static $host = "localhost";
    private static $username = "root";
    private static $password = "subilan1999";
    private $conn;
    public function __construct(string $dbname = "monologue") {
        $this->$conn = new mysqli(self::$host, self::$username, self::$password, $dbname);
        return $this->conn;
    }

    public function done() {
        return empty($this->conn->error);
    }
}