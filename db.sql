create database civic;
use civic ;
CREATE TABLE user (
    name VARCHAR(100),
    email VARCHAR(100) PRIMARY KEY,
    password VARCHAR(255),
    profile_photo VARCHAR(255)
);

CREATE TABLE admin (
    username VARCHAR(100) PRIMARY KEY,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE authority (
    authority_name VARCHAR(100) PRIMARY KEY,
    department VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
);

select * from user;
delete from user where name = "HemmanthG";
CREATE TABLE complaints (
    complaint_no INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(100) NOT NULL,
    issue_type VARCHAR(100) NOT NULL,
    description TEXT,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    status VARCHAR(50) DEFAULT 'Pending',
    assigned_to VARCHAR(100),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_email) REFERENCES user(email),
    FOREIGN KEY (assigned_to) REFERENCES authority(authority_name)
);
	

 