CREATE DATABASE event_manager;

USE event_manager;

CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(255) NOT NULL,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    place VARCHAR(255),
    category_type VARCHAR(100),
    priority ENUM('Low', 'Medium', 'High') DEFAULT 'Medium'
);
