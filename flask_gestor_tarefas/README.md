# Projeto Intermediário - Flask + SQLite

Este é um projeto intermediário completo usando:

- **Python + Flask** no backend
- **SQLite** como banco de dados
- **HTML + CSS + JavaScript** no frontend

## Funcionalidades

- Cadastro de tarefas com título, descrição e prioridade
- Listagem de tarefas ordenadas por data de criação
- Filtro por status (todas, pendentes, concluídas)
- Busca por texto no título ou descrição
- Marcar tarefa como concluída/pendente (AJAX)
- Exclusão de tarefa
- Cards de estatísticas (total, concluídas e pendentes)

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
python app.py
```

Depois, abra: `http://127.0.0.1:5000`

## Estrutura

```text
flask_gestor_tarefas/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## Próximos passos sugeridos

- Implementar autenticação de usuário
- Adicionar edição de tarefa
- Criar paginação
- Publicar no Render ou Railway
