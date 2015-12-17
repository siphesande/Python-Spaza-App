DROP TABLE IF EXISTS `users`;


CREATE TABLE users (
    id INT(11) AUTO_INCREMENT PRIMARY KEY, 
    username VARCHAR(20), 
    password VARCHAR(100), 
    email VARCHAR(50), 
    settings VARCHAR(32500),
    tracking VARCHAR (32500),
    rank INT(3)
    );

