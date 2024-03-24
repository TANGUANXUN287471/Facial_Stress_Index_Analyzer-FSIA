<?php

include_once("dbconnect.php");

// Retrieve form data
$user_name = $_POST['user_name'];
$user_phone = $_POST['user_phone'];
$user_email = $_POST['user_email'];
$user_password = $_POST['user_password'];

// Hash the password using bcrypt
$hashed_password = password_hash($user_password, PASSWORD_BCRYPT);

// Prepare and bind statement
$stmt = $conn->prepare("INSERT INTO user_table (user_name, user_phone, user_email, user_password) VALUES (?, ?, ?, ?)");
$stmt->bind_param("ssss", $user_name, $user_phone, $user_email, $hashed_password);

// Execute the statement
if ($stmt->execute() === TRUE) {
    echo "Registration successful";
} else {
    echo "Error: " . $conn->error;
}

// Close connection
$conn->close();
?>
