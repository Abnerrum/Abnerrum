<?php
require_once __DIR__ . '/includes/functions.php';
$items = getCartItemsDetailed();

if (count($items) === 0) {
    setFlash('error', 'Adicione itens ao carrinho antes do checkout.');
    header('Location: index.php');
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $pedidoId = finalizeOrder($_POST['nome'] ?? '', $_POST['email'] ?? '', $_POST['endereco'] ?? '');
    if ($pedidoId) {
        header('Location: confirmation.php?pedido=' . $pedidoId);
        exit;
    }
    setFlash('error', 'Dados inválidos ou erro ao processar pedido.');
}

require __DIR__ . '/includes/header.php';
?>
<h1>Checkout</h1>
<p>Total do pedido: <strong>R$ <?php echo number_format(cartTotal(), 2, ',', '.'); ?></strong></p>
<form method="post" class="checkout-form">
    <label>Nome completo</label>
    <input type="text" name="nome" required>

    <label>E-mail</label>
    <input type="email" name="email" required>

    <label>Endereço</label>
    <textarea name="endereco" required></textarea>

    <button class="btn" type="submit">Pagar (simulação)</button>
</form>
<?php require __DIR__ . '/includes/footer.php'; ?>
