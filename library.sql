CREATE DATABASE IF NOT EXISTS library
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE library;

-- =========================
-- TABELA USUÁRIOS
-- =========================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    tipo ENUM('usuario','funcionario') 
        NOT NULL DEFAULT 'usuario',
    ativo BOOLEAN DEFAULT TRUE,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_tipo (tipo)
);

-- =========================
-- TABELA LIVROS
-- =========================
CREATE TABLE livros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(150) NOT NULL,
    editora VARCHAR(150),
    quantidade_total INT NOT NULL DEFAULT 1 CHECK (quantidade_total >= 0),
    quantidade_disponivel INT NOT NULL DEFAULT 1 CHECK (quantidade_disponivel >= 0),
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_titulo (titulo),
    INDEX idx_autor (autor)
);

-- =========================
-- TABELA EMPRÉSTIMOS
-- =========================
CREATE TABLE emprestimos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_livro INT NOT NULL,
    data_emprestimo DATE NOT NULL,
    data_prevista_devolucao DATE NOT NULL,
    data_devolucao DATE NULL,
    multa DECIMAL(10,2) DEFAULT 0 CHECK (multa >= 0),
    status ENUM('emprestado','devolvido','atrasado')
        DEFAULT 'emprestado',

    CONSTRAINT fk_usuario 
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_livro 
        FOREIGN KEY (id_livro) REFERENCES livros(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    INDEX idx_usuario (id_usuario),
    INDEX idx_livro (id_livro),
    INDEX idx_status (status)
);
DELIMITER $$

CREATE TRIGGER reduzir_estoque
BEFORE INSERT ON emprestimos
FOR EACH ROW
BEGIN
    DECLARE qtd INT;

    SELECT quantidade_disponivel 
    INTO qtd 
    FROM livros 
    WHERE id = NEW.id_livro;

    IF qtd <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Livro indisponível para empréstimo';
    END IF;

    UPDATE livros
    SET quantidade_disponivel = quantidade_disponivel - 1
    WHERE id = NEW.id_livro;
END$$

DELIMITER ;
