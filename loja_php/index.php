<?php
require_once __DIR__ . '/includes/functions.php';
$products = getProducts();
require __DIR__ . '/includes/header.php';
?>
<h1>Produtos em destaque</h1>
<div class="grid">
    <?php foreach ($products as $product): ?>
        <article class="card">
            <img src="<?php echo h($product['imagem']); ?>" alt="<?php echo h($product['nome']); ?>">
            <h2><?php echo h($product['nome']); ?></h2>
            <p><?php echo h($product['descricao']); ?></p>
            <strong>R$ <?php echo number_format((float) $product['preco'], 2, ',', '.'); ?></strong>
            <div class="actions">
                <a class="btn" href="product.php?id=<?php echo (int) $product['id']; ?>">Ver detalhes</a>
            </div>
        </article>
    <?php endforeach; ?>
</div>
<?php require __DIR__ . '/includes/footer.php'; ?>
