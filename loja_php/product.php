<?php
require_once __DIR__ . '/includes/functions.php';
$id = filter_input(INPUT_GET, 'id', FILTER_VALIDATE_INT);
$product = $id ? getProductById($id) : null;

if (!$product) {
    setFlash('error', 'Produto não encontrado.');
    header('Location: index.php');
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $qty = filter_input(INPUT_POST, 'qty', FILTER_VALIDATE_INT);
    $qty = $qty && $qty > 0 ? $qty : 1;

    if (addToCart((int) $product['id'], $qty)) {
        setFlash('success', 'Produto adicionado ao carrinho!');
        header('Location: cart.php');
        exit;
    }
    setFlash('error', 'Não foi possível adicionar o produto.');
}

require __DIR__ . '/includes/header.php';
?>
<article class="product-page">
    <img src="<?php echo h($product['imagem']); ?>" alt="<?php echo h($product['nome']); ?>">
    <div>
        <h1><?php echo h($product['nome']); ?></h1>
        <p><?php echo h($product['descricao']); ?></p>
        <h2>R$ <?php echo number_format((float) $product['preco'], 2, ',', '.'); ?></h2>
        <form method="post" class="inline-form">
            <label>Quantidade:</label>
            <input type="number" min="1" name="qty" value="1">
            <button class="btn" type="submit">Adicionar ao carrinho</button>
        </form>
    </div>
</article>
<?php require __DIR__ . '/includes/footer.php'; ?>
