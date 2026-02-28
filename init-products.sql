CREATE DATABASE IF NOT EXISTS productosdb;
USE productosdb;

CREATE TABLE productos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100),
  precio FLOAT,
  stock INT
);

INSERT INTO productos VALUES(null, "Pan", 2000, 5);