<?php
session_start();

// Database connection
$db = new PDO('mysql:host=localhost;dbname=your_database', 'username', 'password');

// Authentication check
function is_authenticated() {
    return isset($_SESSION['user_id']);
}

// Router
$request = $_SERVER['REQUEST_URI'];

switch ($request) {
    case '/':
        require __DIR__ . '/views/home.php';
        break;
    case '/login':
        require __DIR__ . '/views/login.php';
        break;
    default:
        http_response_code(404);
        require __DIR__ . '/views/404.php';
        break;
}