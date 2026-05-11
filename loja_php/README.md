# Loja PHP (PHP puro + MySQL)

Projeto de e-commerce simples e funcional para rodar no localhost com XAMPP.

## Requisitos
- PHP 8+
- MySQL / MariaDB
- Apache (XAMPP)

## Como rodar (passo a passo)
1. Copie a pasta `loja_php` para `htdocs` do XAMPP.
2. Inicie Apache e MySQL no painel do XAMPP.
3. Abra o phpMyAdmin (`http://localhost/phpmyadmin`).
4. Crie o banco e as tabelas importando o arquivo `database.sql`.
5. Confirme as credenciais em `config/database.php`:
   - host: `127.0.0.1`
   - banco: `loja_php`
   - usuário: `root`
   - senha: (vazia por padrão no XAMPP)
6. Acesse no navegador: `http://localhost/loja_php`.

## Estrutura
- `index.php`: listagem de produtos
- `product.php`: detalhes e adicionar ao carrinho
- `cart.php`: carrinho (atualizar/remover)
- `checkout.php`: checkout com validação
- `confirmation.php`: confirmação de pedido
- `includes/functions.php`: regras de negócio (sessão, carrinho, pedido)
- `config/database.php`: conexão PDO
- `assets/css/style.css`: layout responsivo
- `database.sql`: script completo do banco

## Extra: integração com Stripe/Mercado Pago
Este projeto está com **simulação de pagamento**. Para integrar gateway real, substitua a ação do botão "Pagar" por chamada ao SDK/API antes de `finalizeOrder()`.
