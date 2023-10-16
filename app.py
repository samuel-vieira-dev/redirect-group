from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1) # Para converter URI do postgres para o formato que o SQLAlchemy reconhece
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo para contagem de cliques
class ClickCounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)

# Lista de links de grupos de WhatsApp
whatsapp_groups = [
    "https://chat.whatsapp.com/exemplo1",
    # ... Adicione todos os 10 links aqui
]

@app.route('/')
def index():
    # Obter ou criar contador
    counter = ClickCounter.query.first()
    if not counter:
        counter = ClickCounter()
        db.session.add(counter)

    counter.count += 1
    db.session.commit()

    # Determinar o índice do link com base no número de cliques
    group_index = counter.count // 1000
    if group_index >= len(whatsapp_groups):
        return "Todos os grupos estão cheios!"

    return redirect(whatsapp_groups[group_index])

@app.cli.command("initdb")
def initdb():
    db.create_all()
    print("Database initialized!")


if __name__ == '__main__':
    app.run()
