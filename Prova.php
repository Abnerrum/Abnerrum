<!-- index.php -->
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Empréstimo de Livros</title>
</head>
<body>
    <h1>Sistema de Empréstimo de Livros</h1>
    <form action="processa_emprestimo.php" method="post">
        <label for="livro">Escolha um livro:</label>
        <select name="livro" id="livro">
            <?php
            // Conexão com o banco de dados (ajuste as configurações conforme necessário)
            $servername = "localhost";
            $username = "root";
            $password = "";
            $dbname = "biblioteca";

            $conn = new mysqli($servername, $username, $password, $dbname);
            if ($conn->connect_error) {
                die("Erro na conexão: " . $conn->connect_error);
            }

            // Consulta para obter a lista de livros disponíveis
            $sql = "SELECT id_livro, titulo FROM livros";
            $result = $conn->query($sql);

            if ($result->num_rows > 0) {
                while ($row = $result->fetch_assoc()) {
                    echo "<option value='" . $row["id_livro"] . "'>" . $row["titulo"] . "</option>";
                }
            } else {
                echo "<option value=''>Nenhum livro disponível</option>";
            }

            $conn->close();
            ?>
        </select>
        <input type="submit" value="Emprestar">
    </form>
</body>
</html>

