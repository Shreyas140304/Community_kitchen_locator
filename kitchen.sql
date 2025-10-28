use ngo_listing;
CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,  -- stores hashed password
    email VARCHAR(100) NOT NULL,
    NGO_Name VARCHAR(100) NOT NULL,
    NGO_Regi VARCHAR(50) NOT NULL,
    establish_date DATE NOT NULL,
    contact_Name VARCHAR(100) NOT NULL,
    phone_num VARCHAR(15) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
alter table accounts rename column password to pass;
CREATE TABLE kitchens (
	id INT AUTO_INCREMENT PRIMARY KEY,
    kitchen_name VARCHAR(30) NOT NULL,
    address TEXT NOT NULL,
    zip VARCHAR(10) NOT NULL,
    service_area VARCHAR(20) NOT NULL,
    contact_person VARCHAR(100) NOT NULL,
    contact_phone INT NOT NULL,
    directions TEXT NOT NULL,
    days VARCHAR(10),
    meal_time VARCHAR(10),
    frequency VARCHAR(10),
    special_hours TEXT,
    meal_types VARCHAR(20),
    audience VARCHAR(20),
    capacity VARCHAR(10) NOT NULL,
    sts VARCHAR(10)
);
alter table kitchens modify phone_num VARCHAR(20);
alter table kitchens modify contact_email VARCHAR(50);
alter table kitchens rename column contact_person to contact_Name, rename column contact_phone to phone_num;
alter table kitchens add column contact_email varchar(20) NOT NULL UNIQUE after phone_num;
select * from accounts;
select * from kitchens;
describe table kitchens;
update kitchens set kitchen_name="saidham", address="bhakti park mmdc colony", zip="400011", service_area="parel", contact_Name="sahil", phone_num="13265454353",
                    contact_email="nkjdn@abc.com", directions="wheelchair", days='["Mon", "Tue", "Wed"]', meal_time="12:00 PM", frequency="daily", special_hours="closed",
                    meal_types='["Hot Meals", "Packed Lunches"]', audience='["Seniors", "Children"]', capacity="200", sts="active"
                    WHERE id ;
                    
select id from kitchens where kitchen_name = "saidham" ;

CREATE TABLE kitchen_feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    detail VARCHAR(255),  -- Kitchen name or location
    rating INT CHECK (rating BETWEEN 1 AND 5), 
    comments TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select * from kitchen_feedback;
-- For MySQL
-- For MySQL
SELECT CONSTRAINT_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE TABLE_NAME = 'kitchen_feedback' AND CONSTRAINT_TYPE = 'CHECK';

alter table kitchen_feedback drop constraint kitchen_feedback_chk_1;
alter table kitchen_feedback add constraint chck_ratings check(rating BETWEEN 1 AND 10);