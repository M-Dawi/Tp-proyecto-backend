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
    estado ENUM('confirmada', 'cancelada', 'completada') NOT NULL DEFAULT 'confirmada',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reservas_socio FOREIGN KEY (id_socio) REFERENCES socios(id) ON DELETE RESTRICT ON UPDATE CASCADE
);
-- Lo dejo comentado hasta que se creen las tablas de socios y canchas
-- CONSTRAINT fk_reservas_cancha FOREIGN KEY (id_cancha) REFERENCES canchas(id) ON DELETE RESTRICT ON UPDATE CASCADE,

-- Datos iniciales de prueba para reservas
INSERT INTO reservas (id_cancha, id_socio, fecha, hora_inicio, hora_fin, monto_total, estado)
VALUES 
(1, 1, '2026-10-20 18:00:00.000000', '2026-10-20 19:00:00.000000', 15000.00, 15000.00, 'confirmada');
-- (1, 1, '2026-09-20', '18:00:00', '19:00:00', 15000.00, 'confirmada');
