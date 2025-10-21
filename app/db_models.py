from . import db

class ClienteDB(db.Model):

    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    agencia = db.Column(db.String(10), nullable=False)
    conta = db.Column(db.String(10), nullable=False)
    tipo_conta = db.Column(db.String(19), nullable=False)
    cartao_credito = db.Column(db.String(20), nullable=True)
    bandeira_cartao_credito = db.Column(db.String(20), nullable=True)
    cartao_debito = db.Column(db.String(19), nullable=False)

    def __repr__(self):
        return f'<Cliente {self.nome}>'