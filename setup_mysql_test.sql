CREATE USER 'hbnb_test'@'localhost' IDENTIFIED WITH mysql_native_password BY 'hbnb_test_pwd';

CREATE DATABASE IF NOT EXISTS hbnb_test_db;

USE hbnb_test_db;

GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost' WITH GRANT OPTION;

GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

