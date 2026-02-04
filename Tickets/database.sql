CREATE DATABASE sistema_tickets;
USE sistema_tickets;

CREATE TABLE tickets (
    id_ticket INT AUTO_INCREMENT PRIMARY KEY,
    solicitante VARCHAR(100) NOT NULL,
    assunto VARCHAR(100) NOT NULL,
    problema TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'Aberto',
    data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,
    responsavel VARCHAR(100),
    comentarios JSON
);