CREATE DATABASE IF NOT EXISTS gestion_deportiva;
USE gestion_deportiva;

-- Crear la tabla de deportes
CREATE TABLE IF NOT EXISTS deportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);
-- Insertar datos a deportes
INSERT INTO deportes (id, nombre) VALUES 
(1, 'Fútbol'),
(2, 'Tenis'),
(3, 'Pádel')
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre);
-- Crear tabla de canchas
 CREATE TABLE IF NOT EXISTS canchas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_deporte INT NOT NULL,
    precio_hora INT NOT NULL,
    techada BOOLEAN NOT NULL DEFAULT FALSE,
    activa BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_canchas_deporte FOREIGN KEY (id_deporte) REFERENCES deportes(id)
);

-- Datos ficticios de prueba para canchas
INSERT INTO canchas (nombre, id_deporte, precio_hora, techada, activa) VALUES
('Cancha 1 - Fútbol 5', 1, 1000000, FALSE, TRUE),
('Cancha 2 - Tenis', 2, 800000, TRUE, TRUE),
('Cancha 3 - Pádel', 3, 900000, TRUE, TRUE);

-- Crear tabla de socios
CREATE TABLE IF NOT EXISTS socios (
   id INT AUTO_INCREMENT PRIMARY KEY,
   nombre VARCHAR (150) NOT NULL,
   email VARCHAR (150) NOT NULL UNIQUE,
   activo BOOLEAN NOT NULL DEFAULT TRUE
);

-- Datos iniciales de prueba para socios
INSERT INTO socios (nombre, email, activo)
VALUES 
('Juan Perez', 'juan.perez@gmail.com', TRUE),
('Maria Gonzalez', 'maria.gonzalez@gmail.com', TRUE),
('Carlos Rodriguez', 'carlos.rodriguez@gmail.com', TRUE);

-- Crear tabla de reservas
CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cancha INT NOT NULL,
    id_socio INT NOT NULL,
    /* dejo comentado para marcar la correccion
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    monto_total DECIMAL(10, 2) NOT NULL,*/
    fecha_hora_inicio DATETIME(6) NOT NULL,
    fecha_hora_fin DATETIME(6) NOT NULL,
    precio_hora DECIMAL(10, 2) NOT NULL,
    precio_total DECIMAL(10, 2) NOT NULL,
    estado ENUM('confirmada', 'cancelada', 'finalizada') NOT NULL DEFAULT 'confirmada',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reservas_socio FOREIGN KEY (id_socio) REFERENCES socios(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_reservas_cancha FOREIGN KEY (id_cancha) REFERENCES canchas(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_reservas_cancha (id_cancha, estado),
    INDEX idx_reservas_socio (id_socio, estado)
);

-- Datos iniciales de prueba para reservas
INSERT INTO reservas (id_cancha, id_socio, fecha_hora_inicio, fecha_hora_fin, precio_hora, precio_total, estado)
VALUES (1, 1, '2026-10-20 18:00:00.000000', '2026-10-20 19:00:00.000000', 15000.00, 15000.00, 'confirmada');
-- (1, 1, '2026-09-20', '18:00:00', '19:00:00', 15000.00, 'confirmada');
