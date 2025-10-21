from flask import Flask, jsonify
from flasgger import Flasgger
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import getenv

from app.model.cliente_model import ClienteCreate, ClienteUpdate, Cliente as ClienteSchema

db = SQLAlchemy()
migrate = Migrate()

class Config:
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL', 'postgresql://usuario:senha@localhost/meu_banco')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' 
    WTF_CSRF_ENABLED = False

def create_app(config_class=Config):
    app = Flask(__name__)
    
    app.config.from_object(config_class) 

    db.init_app(app)
    migrate.init_app(app, db)

    template = {
        "swagger": "2.0",
        "info": {
            "title": "API do Desafio Técnico - Clientes",
            "description": "API para gestão de clientes, parte do desafio técnico.",
            "version": "1.0.0"
        },
        "host": "localhost:5000",  
        "basePath": "/",  
        "schemes": [
            "http",
            "httpss"
        ],
        "definitions": {
            "Cliente": ClienteSchema.model_json_schema(),
            "ClienteCreate": ClienteCreate.model_json_schema(),
            "ClienteUpdate": ClienteUpdate.model_json_schema()
        }
    }

    Flasgger(app, template=template)

    from .controller.cliente_controller import cliente_bp
    app.register_blueprint(cliente_bp)

    with app.app_context():
        from . import db_models

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "success": False,
            "message": "Recurso não encontrado",
            "error": "O endpoint solicitado não existe."
        }), 404

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        return jsonify({
            "success": False,
            "message": "Ocorreu um erro inesperado no servidor",
            "error": "Internal Server Error"
        }), 500
    
    return app