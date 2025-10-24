CREATE DATABASE communityKitchenLocator;
USE communityKitchenLocator;
CREATE TABLE ngo_registration (
    ngo_id INT AUTO_INCREMENT PRIMARY KEY,
    ngo_name VARCHAR(255) NOT NULL,
    registration_number VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    contact_number VARCHAR(15),
    email_address VARCHAR(150) UNIQUE,
    address_line VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(10),
    postal_code VARCHAR(10),
    date_of_establishment DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE ngo_kitchens (
    kitchen_id INT AUTO_INCREMENT PRIMARY KEY,
    ngo_id INT NOT NULL,
    kitchen_name VARCHAR(200) NOT NULL,
    address VARCHAR(255),
    zip_code VARCHAR(10),
    service_area VARCHAR(255),
    contact_person VARCHAR(100),
    contact_phone VARCHAR(20),
    contact_email VARCHAR(150),
    directions TEXT,
    days_open VARCHAR(100),          -- "Mon, Tue, Wed, Fri"
    meal_serving_time VARCHAR(100),  -- "12 PM - 2 PM"
    frequency VARCHAR(50),           -- "Daily", "Weekly"
    special_hours TEXT,              -- "Closed on holidays"
    meal_types VARCHAR(255),         -- "Hot Meals, Packed Lunches, Groceries"
    target_audience VARCHAR(255),    -- "Families, Seniors, Homeless"
    capacity VARCHAR(50),            -- "500 meals/day"
    status ENUM('Active', 'Inactive') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ngo_id) REFERENCES ngo_registration(ngo_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
CREATE USER 'flaskuser'@'localhost' IDENTIFIED BY 'flaskuser@2025';
GRANT ALL PRIVILEGES ON communityKitchenLocator.* TO 'flaskuser'@'localhost';
FLUSH PRIVILEGES;

SHOW TABLES;
DESCRIBE ngo_registration;
DESCRIBE ngo_kitchens;


