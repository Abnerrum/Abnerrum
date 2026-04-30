# Smart Tracker - Monitor de Preços Automatizado

Projeto em Flask para monitorar preços de produtos e disparar alertas por e-mail/WhatsApp.

## Recursos
- Cadastro de produto (URL, preço alvo e contato).
- Verificação manual do preço via scraping (Amazon/Mercado Livre como exemplos de seletores).
- Histórico de preços em SQLite.
- Geração de gráfico simples com Matplotlib.
- Alerta por e-mail (SMTP) e placeholder para WhatsApp/Twilio.

## Como rodar
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:5000`.

## Variáveis de ambiente para e-mail
- `SMTP_SERVER`
- `SMTP_PORT` (padrão 587)
- `SMTP_USER`
- `SMTP_PASS`
- `FLASK_SECRET_KEY`
- `DATABASE_PATH`

## Próximo passo
Adicione um job com APScheduler para chamar verificações de hora em hora.
