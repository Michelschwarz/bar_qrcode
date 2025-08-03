from app import db
from models import Produto
from flask import Flask

# Cria o contexto da aplicação Flask manualmente
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

with app.app_context():
    produtos = [
        Produto(nome="Cerveja", categoria="Bebida", preco=7.50),
        Produto(nome="Refrigerante", categoria="Bebida", preco=5.00),
        Produto(nome="Porção de Batata", categoria="Comida", preco=18.00),
        Produto(nome="X-Burguer", categoria="Comida", preco=22.00),
    ]

    db.session.add_all(produtos)
    db.session.commit()
    print("✅ Produtos adicionados com sucesso!")
