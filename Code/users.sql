-- create database users;
-- USE users;
-- create table user (id INTEGER AUTO_INCREMENT PRIMARY KEY,name VARCHAR(100) NOT NULL,email VARCHAR(100) NOT NULL UNIQUE,
--     password VARCHAR(255) NOT NULL,username VARCHAR(50) NOT NULL UNIQUE,phno VARCHAR(15),
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );
-- select *  from user;
-- Delete FROM user WHERE id = 3;

-- CREATE TABLE IF NOT EXISTS subscription (
--     subscription_id INTEGER AUTO_INCREMENT PRIMARY KEY,
--     plan_name VARCHAR(100) NOT NULL,
--     price DECIMAL(10, 2) NOT NULL,
--     duration VARCHAR(50) NOT NULL,
--     features TEXT,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );


-- CREATE TABLE IF NOT EXISTS user_subscription (
--     user_id INTEGER NOT NULL,
--     subscription_id INTEGER NOT NULL,
--     start_date DATE NOT NULL,
--     end_date DATE,
--     PRIMARY KEY (user_id, subscription_id),
--     FOREIGN KEY (user_id) REFERENCES user(id),
--     FOREIGN KEY (subscription_id) REFERENCES subscription(subscription_id)
-- );

-- Select the database
-- USE users;

-- Insert data into the subscription table
-- INSERT INTO subscription (plan_name, price, duration, features) VALUES
-- ('Basic Plan', 9.99, '1 month', 'Chat with PDF, Basic AI Tools, Limited Support'),
-- ('Standard Plan', 19.99, '1 month', 'Chat with PDF, Advanced AI Tools, Priority Support, Access to New Features'),
-- ('Premium Plan', 29.99, '1 month', 'Chat with PDF, Full AI Tools, 24/7 Premium Support, Early Access to Beta Features, Custom AI Model Training');

-- select * from subscription; 

-- CREATE TABLE IF NOT EXISTS pdfs (
--     pdf_id INT AUTO_INCREMENT PRIMARY KEY,
--     user_id INT,
--     pdf_name VARCHAR(255),
--     uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (user_id) REFERENCES user(user_id)
-- );

-- History table
-- CREATE TABLE IF NOT EXISTS history (
--     history_id INT AUTO_INCREMENT PRIMARY KEY,
--     user_id INT NOT NULL,
--     pdf_id INT NOT NULL,
--     question TEXT NOT NULL,
--     answer TEXT NOT NULL,
--     timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (user_id) REFERENCES user(user_id),
--     FOREIGN KEY (pdf_id) REFERENCES pdfs(pdf_id)
-- );

-- ALTER TABLE user CHANGE id user_id INTEGER AUTO_INCREMENT;
-- ALTER TABLE user ADD PRIMARY KEY (user_id);

-- USE users;
-- select *  from user;
-- select *  from subscription;
-- select *  from pdfs;
-- select *  from history;
-- select *  from user_subscription;

-- update user set password=123 where user_id=1;

-- SET SQL_SAFE_UPDATES = 0;
-- SET FOREIGN_KEY_CHECKS = 0;
-- DELETE FROM user_subscription where user_id=1;
-- SET FOREIGN_KEY_CHECKS = 1;
-- SET SQL_SAFE_UPDATES = 1;

-- SELECT h.history_id, h.question, h.answer, h.timestamp, p.pdf_name FROM history h
-- JOIN pdfs p ON h.pdf_id = p.pdf_id WHERE h.user_id = 1 ORDER BY h.timestamp DESC;

-- DELETE FROM history;
-- TRUNCATE TABLE history;
-- TRUNCATE TABLE user_subscription;
