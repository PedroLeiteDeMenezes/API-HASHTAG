from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Webhook(db.Model):
    __tablename__ = 'webhook'  # Nome da tabela

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    def __init__(self, status, email):
        self.status = status
        self.email = email

    def __repr__(self):
        return f"<Webhook {self.id}: {self.email} - {self.status}>"
