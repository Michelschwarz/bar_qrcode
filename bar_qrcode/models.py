from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bar.db'
db = SQLAlchemy(app)

class Mesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    comandas = db.relationship('Comanda', backref='mesa', lazy=True)

class Comanda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mesa_id = db.Column(db.Integer, db.ForeignKey('mesa.id'), nullable=False)
    aberta_em = db.Column(db.DateTime, default=datetime.utcnow)
    fechada = db.Column(db.Boolean, default=False)
    pedidos = db.relationship('Pedido', backref='comanda', lazy=True)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50))
    preco = db.Column(db.Float, nullable=False)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comanda_id = db.Column(db.Integer, db.ForeignKey('comanda.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    produto = db.relationship('Produto')