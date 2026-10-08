CREATE DATABASE IF NOT EXISTS cadastro_db;
USE cadastro_db;

-- Cria a tabela de usuários quando o banco é inicializado pela primeira vez.
CREATE TABLE IF NOT EXISTS usuarios (
    -- Identificador numérico gerado automaticamente.
    id INT AUTO_INCREMENT PRIMARY KEY,
    -- Nome do usuário; preenchimento obrigatório.
    nome VARCHAR(100) NOT NULL,
    -- E-mail do usuário; preenchimento obrigatório e não pode se repetir.
    email VARCHAR(150) NOT NULL UNIQUE,
    -- Data e hora do cadastro, preenchidas pelo próprio MySQL.
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cria a tabela de cadastros (responsável + sneaker)
CREATE TABLE IF NOT EXISTS cadastros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_responsavel VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(150) NOT NULL,
    sneaker_nome VARCHAR(100) NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    tipo VARCHAR(50),
    tamanho VARCHAR(10),
    cor VARCHAR(50),
    observacoes TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
