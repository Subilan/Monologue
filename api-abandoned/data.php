<?php

include "libraries.php";

require_once "functions/database.php";

$action = $_POST["action"];
$method = $_POST["method"];
$data = $_POST["data"];

$db = new DBController();

switch ($method) {
    case "COMMIT":
        switch ($action) {
            case "logue":
                extract($data);
                $date = date("Y/m/d");
                $extdate = date("D M d Y H:i:s O");
                $db->query("INSERT INTO Logue (date, extdate, title, contents)
                VALUES ($date, $extdate, $title, $contents)");
                if ($db->done()) {
                    echo "ok";
                } else {
                    echo $db->error;
                }
                break;
        }
        break;

    case "GET":
        switch ($action) {
            case "logue-by-date":
                extract($data);
                switch ($type) {
                    case "by-date":
                        $r = $db->query("SELECT * FROM Logue WHERE date='$date'");
                        break;

                    case "initial":
                        $r = $db->query("SELECT * FROM Logue LIMIT 0,20");
                        break;

                }
                $r = $r->fetch_all(MYSQLI_ASSOC);
                // 烧脑循环
                $arr = [];
                foreach ($r as $value) {
                    array_push($value["date"], $value);
                }
                if ($db->done()) {
                    echo json_encode($r, JSON_UNESCAPED_UNICODE);
                } else {
                    echo $db->error();
                }
        }
}
