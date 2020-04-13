<?php

require "libraries.php";
require dir . "/functions/database.php";

$action = $_POST["action"];
$method = $_POST["method"];
$data = $_POST["data"];

$db = new db();

switch ($method) {
    case "COMMIT":
        switch ($action) {
            case "logue":
                extract($data);
                $date = date("Y/m/d");
                $db->query("INSERT INTO Logue (date, title, content)
                VALUES ($date, $title, $content)");
                if ($db->done()) {
                    echo "ok";
                } else {
                    echo $db->error;
                }
            break;
        }
}