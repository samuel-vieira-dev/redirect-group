from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import logging

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1) # Para converter URI do postgres para o formato que o SQLAlchemy reconhece
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

logging.basicConfig(level=logging.INFO)

# Modelo para contagem de cliques
class ClickCounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)

# Lista de links de grupos de WhatsApp
whatsapp_groups = [
    "https://chat.whatsapp.com/I8TonTdCBsI5Q4g9Lo9yrX",
    "https://chat.whatsapp.com/GtO9g9iRqafGvceAVLbtCv",
    "https://chat.whatsapp.com/IQOeiQdkhxW94Opo8Izn08",
    "https://chat.whatsapp.com/E4qoYnIDXr6COZXaxu5Yww",
    "https://chat.whatsapp.com/GyQQGcfOLrwKZtQOIRGu6p",
    "https://chat.whatsapp.com/FF30fN2CGdR1sN2V96INxx",
    "https://chat.whatsapp.com/L1Y2VpM5Ozx9MsKwI0jRD3",
    "https://chat.whatsapp.com/DSKZhxJoBz1HLIXelR2lBJ",
    "https://chat.whatsapp.com/FLOSqqEMCMpLKw8PhvON4v",
    "https://chat.whatsapp.com/Kt15LK05zogJ0AnLqP4Lv1",
]

@app.route('/')
def index():
    # Obter ou criar contador
    counter = ClickCounter.query.first()
    if not counter:
        counter = ClickCounter()
        db.session.add(counter)
        db.session.commit()


    counter.count += 1
    db.session.commit()

    group_index = counter.count // 1
    clicks_left = 1000 - (counter.count % 1000)

    if group_index >= len(whatsapp_groups):
        return "Todos os grupos estão cheios!"

    logging.info(f"Total cliques: {counter.count}")
    logging.info(f"Usando link do grupo {group_index + 1}: {whatsapp_groups[group_index]}")
    logging.info(f"Faltam {clicks_left} cliques para trocar de grupo")

    return redirect(whatsapp_groups[group_index])

@app.cli.command("initdb")
def initdb():
    db.create_all()
    print("Database initialized!")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
