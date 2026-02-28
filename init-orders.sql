CREATE DATABASE IF NOT EXISTS ordenesdb;
use ordenesdb;

CREATE TABLE IF NOT EXISTS ordenes (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario varchar(255),
    correo varchar(255),
    total FLOAT
);

INSERT INTO ordenes VALUES(null, "juan", "juan@gmail.com", 20000);

