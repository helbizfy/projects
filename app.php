<?php

 $email = $_POST['email'];

$host = "localhost";
$dbusername = "root";
$dbpassword = "";
$dbname = "newsletter_emails";

$conn = new mysqli($host, $dbusername, $dbpassword, $dbname);

if($conn->connect_error){
    die("Connect error".$conn->connect_error);
} else {
    $stmt = $conn->prepare("INSERT INTO newsletter_emails(email) values($email)");
    $stmt->exacute();
    echo "New record insterted";
    $stmt->close();
    $conn->close();
}

?>
