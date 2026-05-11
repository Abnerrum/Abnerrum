CREATE DATABASE IF NOT EXISTS loja_php CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE loja_php;

CREATE TABLE IF NOT EXISTS produtos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  descricao TEXT NOT NULL,
  preco DECIMAL(10,2) NOT NULL,
  imagem VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS pedidos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  cliente_nome VARCHAR(120) NOT NULL,
  cliente_email VARCHAR(120) NOT NULL,
  endereco TEXT NOT NULL,
  total DECIMAL(10,2) NOT NULL,
  status VARCHAR(30) NOT NULL,
  criado_em DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS pedido_itens (
  id INT AUTO_INCREMENT PRIMARY KEY,
  pedido_id INT NOT NULL,
  produto_id INT NOT NULL,
  quantidade INT NOT NULL,
  preco_unitario DECIMAL(10,2) NOT NULL,
  CONSTRAINT fk_pedido FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
  CONSTRAINT fk_produto FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

INSERT INTO produtos (nome, descricao, preco, imagem) VALUES
('Fone Bluetooth', 'Fone sem fio com cancelamento de ruído.', 249.90, 'https://picsum.photos/seed/fone/400/300'),
('Teclado Mecânico', 'Teclado ABNT2 com iluminação RGB.', 319.00, 'https://picsum.photos/seed/teclado/400/300'),
('Mouse Gamer', 'Mouse ergonômico de alta precisão.', 159.90, 'https://picsum.photos/seed/mouse/400/300');
