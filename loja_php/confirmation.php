<?php
require_once __DIR__ . '/includes/functions.php';
$pedidoId = filter_input(INPUT_GET, 'pedido', FILTER_VALIDATE_INT);
require __DIR__ . '/includes/header.php';
?>
<h1>Pedido confirmado 🎉</h1>
<?php if ($pedidoId): ?>
    <p>Seu pagamento foi aprovado e o pedido #<?php echo (int) $pedidoId; ?> foi registrado com sucesso.</p>
<?php else: ?>
    <p>Pedido finalizado com sucesso.</p>
<?php endif; ?>
<a class="btn" href="index.php">Voltar à loja</a>
<?php require __DIR__ . '/includes/footer.php'; ?>
