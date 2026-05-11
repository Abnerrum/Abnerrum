<?php
$flash = getFlash();
$cartCount = array_sum(getCart());
?>
<!doctype html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loja PHP</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<header class="topbar">
    <div class="container topbar-inner">
        <a class="brand" href="index.php">Loja PHP</a>
        <a class="cart-link" href="cart.php">🛒 Carrinho (<?php echo $cartCount; ?>)</a>
    </div>
</header>
<main class="container">
    <?php if ($flash): ?>
        <div class="alert alert-<?php echo h($flash['type']); ?>"><?php echo h($flash['message']); ?></div>
    <?php endif; ?>
