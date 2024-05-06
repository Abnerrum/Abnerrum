<!DOCTYPE html>
<html>
<head>
    <title>Inserir Dados na Tabela Filha</title>
</head>
<body>
    <h2>Inserir Dados do cliente</h2>
    <form action="processar_insercao_cliente.php" method="post">
        Valor: <input type="text" name="valor"><br>
        Tabela vendedor(vendedor):
        <select name="id_vendedor">
            <?php
            include 'conexao.php';
            $sql = "SELECT id, nome FROM vendedor";
            $result = $conn->query($sql);
            if ($result->num_rows > 0) {
                while($row = $result->fetch_assoc()) {
                    echo "<option value='" . $row["id"] . "'>" . $row["nome"] . "</option>";
                }
            }
            ?>
        </select><br>
        <input type="submit" value="Inserir">
    </form>
</body>
</html>
