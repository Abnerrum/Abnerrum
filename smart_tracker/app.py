import os
import sqlite3
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret')
DB_PATH = os.getenv('DATABASE_PATH', 'smart_tracker.db')


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.executescript(
        '''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            url TEXT NOT NULL,
            target_price REAL NOT NULL,
            contact_type TEXT NOT NULL,
            contact_value TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            price REAL NOT NULL,
            checked_at TEXT NOT NULL,
            FOREIGN KEY(product_id) REFERENCES products(id)
        );
        '''
    )
    conn.commit()
    conn.close()


def parse_price_from_page(url: str):
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/123.0.0.0 Safari/537.36'
        )
    }
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    title = (soup.find(id='productTitle') or soup.find('h1') or soup.title)
    title_text = title.get_text(strip=True) if title else 'Produto sem título'

    selectors = ['.a-price-whole', '.priceToPay span', '.andes-money-amount__fraction']
    price_text = None
    for selector in selectors:
        tag = soup.select_one(selector)
        if tag and tag.get_text(strip=True):
            price_text = tag.get_text(strip=True)
            break

    if not price_text:
        raise ValueError('Não foi possível localizar o preço com os seletores padrão.')

    normalized = ''.join(ch for ch in price_text if ch.isdigit() or ch in ',.')
    normalized = normalized.replace('.', '').replace(',', '.')
    current_price = float(normalized)
    return title_text, current_price


def save_price(product_id: int, price: float):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO price_history (product_id, price, checked_at) VALUES (?, ?, ?)',
        (product_id, price, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()


def send_email_alert(subject: str, body: str, recipient: str):
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USER')
    smtp_pass = os.getenv('SMTP_PASS')

    if not all([smtp_server, smtp_user, smtp_pass]):
        print('SMTP não configurado. Mensagem simulada:')
        print(body)
        return

    message = MIMEMultipart()
    message['From'] = smtp_user
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, recipient, message.as_string())


def notify_if_needed(product, current_price):
    if current_price <= product['target_price']:
        body = (
            f"Opa! {product['name']} baixou para R$ {current_price:.2f}. "
            f"Corre aqui: {product['url']}"
        )
        if product['contact_type'] == 'email':
            send_email_alert('Alerta de preço', body, product['contact_value'])
        else:
            print('Integração WhatsApp (Twilio) pode ser adicionada aqui:')
            print(body)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        target_price = float(request.form['target_price'])
        contact_type = request.form['contact_type']
        contact_value = request.form['contact_value']

        conn = get_db_connection()
        conn.execute(
            '''
            INSERT INTO products (name, url, target_price, contact_type, contact_value, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (name, url, target_price, contact_type, contact_value, datetime.utcnow().isoformat())
        )
        conn.commit()
        conn.close()
        flash('Produto cadastrado com sucesso!')
        return redirect(url_for('index'))

    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', products=products)


@app.route('/check/<int:product_id>')
def check_product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()

    if not product:
        flash('Produto não encontrado.')
        return redirect(url_for('index'))

    try:
        title, current_price = parse_price_from_page(product['url'])
        if not product['name']:
            conn = get_db_connection()
            conn.execute('UPDATE products SET name = ? WHERE id = ?', (title, product_id))
            conn.commit()
            conn.close()

        save_price(product_id, current_price)
        notify_if_needed(product, current_price)
        flash(f'Preço atual de {title}: R$ {current_price:.2f}')
    except Exception as exc:
        flash(f'Falha ao verificar preço: {exc}')

    return redirect(url_for('index'))


@app.route('/chart/<int:product_id>')
def chart(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    history = conn.execute(
        'SELECT price, checked_at FROM price_history WHERE product_id = ? ORDER BY checked_at',
        (product_id,)
    ).fetchall()
    conn.close()

    if not product or not history:
        flash('Sem histórico para gerar gráfico.')
        return redirect(url_for('index'))

    dates = [datetime.fromisoformat(row['checked_at']) for row in history]
    prices = [row['price'] for row in history]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, prices, marker='o')
    plt.title(f'Histórico de preços - {product["name"]}')
    plt.xlabel('Data/Hora')
    plt.ylabel('Preço (R$)')
    plt.xticks(rotation=35)
    plt.tight_layout()

    os.makedirs('static', exist_ok=True)
    output_path = f'static/chart_{product_id}.png'
    plt.savefig(output_path)
    plt.close()

    return render_template('chart.html', product=product, chart_path=output_path)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
