<?php
require_once __DIR__ . '/includes/functions.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';
    $productId = filter_input(INPUT_POST, 'product_id', FILTER_VALIDATE_INT);

    if ($productId) {
        if ($action === 'remove') {
            updateCartItem($productId, 0);
            setFlash('success', 'Item removido do carrinho.');
        }

        if ($action === 'update') {
            $qty = filter_input(INPUT_POST, 'qty', FILTER_VALIDATE_INT);
            updateCartItem($productId, $qty ?: 1);
            setFlash('success', 'Carrinho atualizado.');
        }
    }
    header('Location: cart.php');
    exit;
}

$items = getCartItemsDetailed();
$total = cartTotal();
require __DIR__ . '/includes/header.php';
?>
<h1>Seu carrinho</h1>
<?php if (count($items) === 0): ?>
    <p>Seu carrinho está vazio.</p>
<?php else: ?>
    <table class="table">
        <tr><th>Produto</th><th>Qtd</th><th>Subtotal</th><th>Ações</th></tr>
        <?php foreach ($items as $item): ?>
            <tr>
                <td><?php echo h($item['product']['nome']); ?></td>
                <td>
                    <form method="post" class="inline-form">
                        <input type="hidden" name="action" value="update">
                        <input type="hidden" name="product_id" value="<?php echo (int) $item['product']['id']; ?>">
                        <input type="number" name="qty" min="1" value="<?php echo (int) $item['qty']; ?>">
                        <button class="btn btn-small" type="submit">Atualizar</button>
                    </form>
                </td>
                <td>R$ <?php echo number_format((float) $item['subtotal'], 2, ',', '.'); ?></td>
                <td>
                    <form method="post">
                        <input type="hidden" name="action" value="remove">
                        <input type="hidden" name="product_id" value="<?php echo (int) $item['product']['id']; ?>">
                        <button class="btn btn-danger btn-small" type="submit">Remover</button>
                    </form>
                </td>
            </tr>
        <?php endforeach; ?>
    </table>
    <h2>Total: R$ <?php echo number_format($total, 2, ',', '.'); ?></h2>
    <a class="btn" href="checkout.php">Ir para checkout</a>
<?php endif; ?>
<?php require __DIR__ . '/includes/footer.php'; ?>
