CREATE DATABASE train_db2;
USE train_db2;

CREATE TABLE train_details (
    train_number VARCHAR(10) PRIMARY KEY,
    train_name VARCHAR(100) NOT NULL,
    origin VARCHAR(50) NOT NULL,
    destination VARCHAR(50) NOT NULL
);

INSERT INTO train_details VALUES 
('101', 'Express Train', 'New York', 'Los Angeles'),
('102', 'City Connector', 'Boston', 'Washington DC'),
('103', 'Coastal Rider', 'San Francisco', 'Seattle');
select *from train_details;