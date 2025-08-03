from flask import Flask, render_template, redirect, url_for, request
from models import db, Mesa, Comanda, Produto, Pedido
import qrcode
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

# Garante que pastas e DB existam
os.makedirs('static/qrcodes', exist_ok=True)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    mesas = Mesa.query.all()
    return render_template('index.html', mesas=mesas)

@app.route('/mesa/<int:mesa_id>', methods=['GET', 'POST'])
def ver_comanda(mesa_id):
    comanda = Comanda.query.filter_by(mesa_id=mesa_id, fechada=False).first()
    if not comanda:
        comanda = Comanda(mesa_id=mesa_id)
        db.session.add(comanda)
        db.session.commit()

    if request.method == 'POST':
        if 'fechar_comanda' in request.form:
            comanda.fechada = True
            db.session.commit()
            return render_template('recibo.html', comanda=comanda, pedidos=comanda.pedidos)
        else:
            produto_id = int(request.form.get('produto_id'))
            quantidade = int(request.form.get('quantidade', 1))

            novo_pedido = Pedido(
                comanda_id=comanda.id,
                produto_id=produto_id,
                quantidade=quantidade
            )
            db.session.add(novo_pedido)
            db.session.commit()
            return redirect(url_for('ver_comanda', mesa_id=mesa_id))

    produtos = Produto.query.all()
    pedidos = Pedido.query.filter_by(comanda_id=comanda.id).all()
    total = sum(p.produto.preco * p.quantidade for p in pedidos)

    return render_template('comanda.html', comanda=comanda, produtos=produtos, pedidos=pedidos, total=total)

@app.route('/produtos')
def lista_produtos():
    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

@app.route('/cadastrar_produto', methods=['POST'])
def cadastrar_produto():
    nome = request.form.get('nome')
    categoria = request.form.get('categoria')
    preco = request.form.get('preco')
    if nome and preco:
        produto = Produto(
            nome=nome,
            categoria=categoria or "Sem categoria",
            preco=float(preco.replace(',', '.'))
        )
        db.session.add(produto)
        db.session.commit()
    return redirect(url_for('lista_produtos'))

def gerar_qrcode(mesa_id):
    url = f"http://localhost:5000/mesa/{mesa_id}"
    img = qrcode.make(url)
    img_path = f'static/qrcodes/mesa_{mesa_id}.png'
    img.save(img_path)

if __name__ == '__main__':
    app.run(debug=True)
