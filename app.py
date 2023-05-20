from flask import Flask , render_template , request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///webhooks.db'
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

db = SQLAlchemy(app)


# Tabela para armazenar os webhooks registrados
class Webhook(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    status = db.Column(db.String(20) , nullable=False)
    email = db.Column(db.String(50) , nullable=False)

    def __init__(self , status , email):
        self.status = status
        self.email = email

    def __repr__(self):
        return f"<Webhook {self.id}: {self.email} - {self.status}>"


# Rota para a página inicial
@app.route('/')
def index():
    return render_template('/index.html')


# Rota para a página de cadastro
@app.route('/cadastro' , methods=[ 'GET' , 'POST' ])
def cadastro():
    if request.method == 'POST':
        token = request.form.get('token')
        email = request.form.get('email')

        if token == 'uhdfaAADF123':
            webhook = Webhook(status='aprovado' , email=email)
            db.session.add(webhook)
            db.session.commit( )
            print(f"Liberar acesso do e-mail: {email}")
            return 'Cadastro bem-sucedido!'
        else:
            webhook = Webhook(status='falha' , email=email)
            db.session.add(webhook)
            db.session.commit( )
            print(f"Tirar acesso do e-mail: {email}")
            return 'Falha no cadastro.'
    else:
        return render_template('/cadastro.html')


# Rota para a página de tratativas
@app.route('/tratativas')
def tratativas():
    webhooks = Webhook.query.all( )
    return render_template('/tratativas.html', webhooks=webhooks)


# Rota para enviar mensagem
@app.route('/enviar_mensagem/<int:id>')
def enviar_mensagem(id):
    webhook = Webhook.query.get(id)
    if webhook:
        print(f"Enviar mensagem de boas vindas para o email: {webhook.email}")
        return 'Mensagem enviada com sucesso!'
    else:
        return 'Webhook não encontrado.'


# Rota para tirar acesso
@app.route('/tirar_acesso/<int:id>')
def tirar_acesso(id):
    webhook = Webhook.query.get(id)
    if webhook:
        print(f"Tirar acesso do e-mail: {webhook.email}")
        return 'Acesso removido com sucesso!'
    else:
        return 'Webhook não encontrado.'


# Rota para liberar acesso
@app.route('/liberar_acesso/<int:id>')
def liberar_acesso(id):
    webhook = Webhook.query.get(id)
    if webhook:
        print(f"Liberar acesso do e-mail: {webhook.email}")
        return 'Acesso liberado com sucesso!'
    else:
        return 'Webhook não encontrado.'


if __name__ == '__main__':
    app.run(debug=True)
