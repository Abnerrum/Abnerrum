<?php
require_once __DIR__ . '/../config/database.php';

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

function h(string $value): string
{
    return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}

function setFlash(string $type, string $message): void
{
    $_SESSION['flash'] = ['type' => $type, 'message' => $message];
}

function getFlash(): ?array
{
    if (!isset($_SESSION['flash'])) {
        return null;
    }
    $flash = $_SESSION['flash'];
    unset($_SESSION['flash']);

    return $flash;
}

function getProducts(): array
{
    $stmt = getPDO()->query('SELECT id, nome, descricao, preco, imagem FROM produtos ORDER BY id DESC');
    return $stmt->fetchAll();
}

function getProductById(int $id): ?array
{
    $stmt = getPDO()->prepare('SELECT id, nome, descricao, preco, imagem FROM produtos WHERE id = :id LIMIT 1');
    $stmt->execute(['id' => $id]);
    $product = $stmt->fetch();
    return $product ?: null;
}

function getCart(): array
{
    return $_SESSION['cart'] ?? [];
}

function saveCart(array $cart): void
{
    $_SESSION['cart'] = $cart;
}

function addToCart(int $productId, int $qty = 1): bool
{
    if ($qty < 1) {
        return false;
    }

    $product = getProductById($productId);
    if (!$product) {
        return false;
    }

    $cart = getCart();
    $cart[$productId] = ($cart[$productId] ?? 0) + $qty;
    saveCart($cart);

    return true;
}

function updateCartItem(int $productId, int $qty): void
{
    $cart = getCart();
    if ($qty <= 0) {
        unset($cart[$productId]);
    } else {
        $cart[$productId] = $qty;
    }
    saveCart($cart);
}

function getCartItemsDetailed(): array
{
    $items = [];
    $cart = getCart();

    foreach ($cart as $productId => $qty) {
        $product = getProductById((int) $productId);
        if (!$product) {
            continue;
        }
        $subtotal = $product['preco'] * $qty;
        $items[] = [
            'product' => $product,
            'qty' => $qty,
            'subtotal' => $subtotal,
        ];
    }

    return $items;
}

function cartTotal(): float
{
    $total = 0;
    foreach (getCartItemsDetailed() as $item) {
        $total += $item['subtotal'];
    }
    return $total;
}

function finalizeOrder(string $nome, string $email, string $endereco): ?int
{
    $nome = trim($nome);
    $email = trim($email);
    $endereco = trim($endereco);

    if ($nome === '' || !filter_var($email, FILTER_VALIDATE_EMAIL) || $endereco === '') {
        return null;
    }

    $items = getCartItemsDetailed();
    if (count($items) === 0) {
        return null;
    }

    $pdo = getPDO();
    $pdo->beginTransaction();

    try {
        $total = cartTotal();
        $stmtPedido = $pdo->prepare('INSERT INTO pedidos (cliente_nome, cliente_email, endereco, total, status, criado_em) VALUES (:nome, :email, :endereco, :total, :status, NOW())');
        $stmtPedido->execute([
            'nome' => $nome,
            'email' => $email,
            'endereco' => $endereco,
            'total' => $total,
            'status' => 'pago',
        ]);

        $pedidoId = (int) $pdo->lastInsertId();

        $stmtItem = $pdo->prepare('INSERT INTO pedido_itens (pedido_id, produto_id, quantidade, preco_unitario) VALUES (:pedido_id, :produto_id, :quantidade, :preco_unitario)');

        foreach ($items as $item) {
            $stmtItem->execute([
                'pedido_id' => $pedidoId,
                'produto_id' => $item['product']['id'],
                'quantidade' => $item['qty'],
                'preco_unitario' => $item['product']['preco'],
            ]);
        }

        $pdo->commit();
        unset($_SESSION['cart']);
        return $pedidoId;
    } catch (Throwable $e) {
        $pdo->rollBack();
        return null;
    }
}
