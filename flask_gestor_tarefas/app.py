from datetime import datetime
from pathlib import Path

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    prioridade = db.Column(db.String(20), nullable=False, default="media")
    concluida = db.Column(db.Boolean, default=False, nullable=False)
    criada_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


def inicializar_banco() -> None:
    with app.app_context():
        db.create_all()


@app.route("/")
def index():
    filtro_status = request.args.get("status", "todas")
    busca = request.args.get("busca", "").strip()

    query = Tarefa.query.order_by(Tarefa.criada_em.desc())

    if filtro_status == "pendentes":
        query = query.filter_by(concluida=False)
    elif filtro_status == "concluidas":
        query = query.filter_by(concluida=True)

    if busca:
        termo = f"%{busca}%"
        query = query.filter(
            db.or_(
                Tarefa.titulo.ilike(termo),
                Tarefa.descricao.ilike(termo),
            )
        )

    tarefas = query.all()
    total = Tarefa.query.count()
    concluidas = Tarefa.query.filter_by(concluida=True).count()

    return render_template(
        "index.html",
        tarefas=tarefas,
        filtro_status=filtro_status,
        busca=busca,
        total=total,
        concluidas=concluidas,
    )


@app.route("/tarefas", methods=["POST"])
def criar_tarefa():
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()
    prioridade = request.form.get("prioridade", "media")

    if not titulo or not descricao:
        flash("Preencha título e descrição para cadastrar a tarefa.", "erro")
        return redirect(url_for("index"))

    tarefa = Tarefa(titulo=titulo, descricao=descricao, prioridade=prioridade)
    db.session.add(tarefa)
    db.session.commit()

    flash("Tarefa criada com sucesso!", "sucesso")
    return redirect(url_for("index"))


@app.route("/tarefas/<int:tarefa_id>/status", methods=["POST"])
def alternar_status(tarefa_id: int):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    tarefa.concluida = not tarefa.concluida
    db.session.commit()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"ok": True, "concluida": tarefa.concluida})

    return redirect(url_for("index"))


@app.route("/tarefas/<int:tarefa_id>/excluir", methods=["POST"])
def excluir_tarefa(tarefa_id: int):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    db.session.delete(tarefa)
    db.session.commit()

    flash("Tarefa removida.", "sucesso")
    return redirect(url_for("index"))


if __name__ == "__main__":
    inicializar_banco()
    app.run(debug=True)
