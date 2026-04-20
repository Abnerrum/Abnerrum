from __future__ import annotations

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "projeto.db"


def conectar() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def inicializar_banco() -> None:
    with conectar() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                concluida INTEGER NOT NULL DEFAULT 0
            )
            """
        )


def criar_tarefa(titulo: str, descricao: str) -> None:
    with conectar() as conn:
        conn.execute(
            "INSERT INTO tarefas (titulo, descricao) VALUES (?, ?)",
            (titulo, descricao),
        )


def listar_tarefas() -> list[sqlite3.Row]:
    with conectar() as conn:
        cursor = conn.execute(
            "SELECT id, titulo, descricao, concluida FROM tarefas ORDER BY id DESC"
        )
        return cursor.fetchall()


def concluir_tarefa(tarefa_id: int) -> bool:
    with conectar() as conn:
        cursor = conn.execute(
            "UPDATE tarefas SET concluida = 1 WHERE id = ?",
            (tarefa_id,),
        )
        return cursor.rowcount > 0


def excluir_tarefa(tarefa_id: int) -> bool:
    with conectar() as conn:
        cursor = conn.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
        return cursor.rowcount > 0


def menu() -> None:
    print("\n=== Projeto Python + SQLite (CRUD de tarefas) ===")
    print("1 - Criar tarefa")
    print("2 - Listar tarefas")
    print("3 - Concluir tarefa")
    print("4 - Excluir tarefa")
    print("0 - Sair")


def executar() -> None:
    inicializar_banco()

    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            titulo = input("Título: ").strip()
            descricao = input("Descrição: ").strip()
            if not titulo or not descricao:
                print("⚠️ Título e descrição são obrigatórios.")
                continue
            criar_tarefa(titulo, descricao)
            print("✅ Tarefa criada com sucesso.")

        elif opcao == "2":
            tarefas = listar_tarefas()
            if not tarefas:
                print("Nenhuma tarefa cadastrada.")
                continue

            for tarefa in tarefas:
                status = "Concluída" if tarefa["concluida"] else "Pendente"
                print(
                    f"[{tarefa['id']}] {tarefa['titulo']} - {tarefa['descricao']} ({status})"
                )

        elif opcao == "3":
            try:
                tarefa_id = int(input("ID da tarefa para concluir: ").strip())
            except ValueError:
                print("⚠️ ID inválido.")
                continue

            if concluir_tarefa(tarefa_id):
                print("✅ Tarefa marcada como concluída.")
            else:
                print("⚠️ Tarefa não encontrada.")

        elif opcao == "4":
            try:
                tarefa_id = int(input("ID da tarefa para excluir: ").strip())
            except ValueError:
                print("⚠️ ID inválido.")
                continue

            if excluir_tarefa(tarefa_id):
                print("✅ Tarefa excluída.")
            else:
                print("⚠️ Tarefa não encontrada.")

        elif opcao == "0":
            print("Até logo!")
            break

        else:
            print("⚠️ Opção inválida.")


if __name__ == "__main__":
    executar()
