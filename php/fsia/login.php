<?php

include_once("dbconnect.php");

// Retrieve form data
$user_email = $_POST['user_email'];
$user_password = $_POST['user_password'];

// Prepare and bind statement
$stmt = $conn->prepare("SELECT * FROM user_table WHERE user_email = ?");
$stmt->bind_param("s", $user_email);

// Execute the statement
$stmt->execute();

// Get result
$result = $stmt->get_result();

// Check if user exists and verify password
if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    if (password_verify($user_password, $row['user_password'])) {
        // Password is correct, user can be logged in
        echo "Login successful";
        // You can also fetch user data from $row array for further processing
    } else {
        echo "Incorrect password";
    }
} else {
    echo "User not found";
}

// Close connection
$conn->close();
?>
