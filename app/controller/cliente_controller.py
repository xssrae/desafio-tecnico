from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app import db
from app.db_models import ClienteDB
from app.model.cliente_model import ClienteCreate, ClienteUpdate, Cliente as ClienteSchema

cliente_bp = Blueprint("clientes", __name__, url_prefix="/clientes")

@cliente_bp.route("/", methods=["GET"]) # GET - Listar todos os clientes (Obrigatório)
def buscar_ou_listar_clientes():
    try:
        nome = request.args.get('nome')

        if nome:
            clientes_db = ClienteDB.query.filter( # Desafio Extra - Buscar clientes por nome pela query cliente?nome=string
                ClienteDB.nome.ilike(f"%{nome}%")
            ).all()
            if not clientes_db:
                return jsonify({
                    "success": False,
                    "message": "Nenhum cliente encontrado",
                    "error": f"Nenhum cliente encontrado contendo '{nome}'"
                }), 404
        else:
            clientes_db = ClienteDB.query.all()
            if not clientes_db:
                return jsonify({"success": True, "message": "Nenhum cliente cadastrado", "data": []}), 200
            
            
        data = [ClienteSchema.model_validate(c).model_dump(exclude_none=True) for c in clientes_db]

        return jsonify({
            "success": True,
            "message": "Clientes encontrados com sucesso",
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erro ao buscar clientes",
            "error": str(e)
        }), 500


@cliente_bp.route("/<int:id>", methods=["GET"]) # Obrigatório - Listar cliente por ID
def buscar_cliente_por_id(id: int):
   
    try:
        cliente_db = db.session.get(ClienteDB, id)
        if not cliente_db:
            return jsonify({
                "success": False,
                "message": "Cliente não encontrado",
                "error": f"Nenhum cliente encontrado com ID {id}"
            }), 404
        return jsonify({
            "success": True,
            "message": "Cliente encontrado com sucesso",
            "data": ClienteSchema.model_validate(cliente_db).model_dump()
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erro ao buscar cliente",
            "error": str(e)
        }), 500


@cliente_bp.route("/", methods=["POST"]) # POST - Criar novo cliente (Extra)
def criar_cliente():
    data = request.get_json()

    if not data:
            return jsonify({
                "success": False,
                "message": "Requisição inválida",
                "error": "Requisição precisa conter dados JSON"
            }), 400
    try:
        cliente_create = ClienteCreate(**data)
    except ValidationError as e:
        return jsonify({
            "success": False,
            "message": "Dados inválidos",
            "errors": e.errors()
        }), 400
    
    from sqlalchemy import or_
    db_cliente_existente = ClienteDB.query.filter(
        or_(
            ClienteDB.cpf == cliente_create.cpf,
            ClienteDB.email == cliente_create.email
        )
    ).first()

    if db_cliente_existente:
        if db_cliente_existente.email == cliente_create.email:
            return jsonify({
                "success": False,
                "message": "Email já cadastrado",
                "error": f"O email já está cadastrado"
            }), 409
        else:
            return jsonify({
                "success": False,
                "message": "CPF já cadastrado",
                "error": f"O CPF já está cadastrado"
            }), 409
    
    novo_cliente = ClienteDB(**cliente_create.model_dump())
    try:
        db.session.add(novo_cliente)
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Cliente criado com sucesso",
            "data": ClienteSchema.model_validate(novo_cliente).model_dump()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Erro ao salvar cliente",
            "error": str(e)
        }), 500


@cliente_bp.route("/<int:id>", methods=["PUT"]) # PUT - Atualizar cliente por ID (Extra)
def atualizar_cliente(id: int):

    cliente_db = ClienteDB.query.filter_by(id=id).first()

    if cliente_db is None:
        return jsonify({
            "success": False,
            "message": "Cliente não encontrado",
            "error": f"Nenhum cliente encontrado com o ID {id}" 
        }), 404
    
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Requisição inválida",
            "error": "Requisição precisa conter dados JSON"
        }), 400
    
    try:
        cliente_update = ClienteUpdate(**data)
    except ValidationError as e:
        return jsonify({
            "success": False,
            "message": "Dados inválidos. Verifique os campos enviados.",
            "errors": e.errors()
        }), 400
    
    try:
        if cliente_update.email is not None and cliente_update.email != cliente_db.email:
            email_existente = ClienteDB.query.filter(
                ClienteDB.email == cliente_update.email, 
                ClienteDB.id != cliente_db.id
            ).first() 

            if email_existente:
                return jsonify({
                    "success": False,
                    "message": "Email já cadastrado",
                    "error": f"O email '{cliente_update.email}' já está cadastrado"
                }), 409
        
        if cliente_update.cpf is not None and cliente_update.cpf != cliente_db.cpf:
            cpf_existente = ClienteDB.query.filter(
                ClienteDB.cpf == cliente_update.cpf, 
                ClienteDB.id != cliente_db.id
            ).first()

            if cpf_existente:
                return jsonify({
                    "success": False,
                    "message": "CPF já cadastrado",
                    "error": f"O CPF '{cliente_update.cpf}' já está cadastrado"
                }), 409

        for key, value in cliente_update.model_dump(exclude_unset=True).items():
            setattr(cliente_db, key, value)
            
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Cliente atualizado com sucesso",
            "data": ClienteSchema.model_validate(cliente_db).model_dump()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao atualizar cliente: {e}") 
        return jsonify({ 
            "success": False,
            "message": "Erro ao atualizar cliente", # Mensagem mais específica
            "error": str(e)
        }), 500

@cliente_bp.route("/<int:id>", methods=["DELETE"]) # DELETE - Deletar cliente por ID (Extra)
def deletar_cliente(id: int):

    cliente = ClienteDB.query.filter_by(id=id).first()

    if cliente is None:
        return jsonify({
            "success": False,
            "message": "Cliente não encontrado",
            "error": f"Nenhum cliente encontrado com o ID informado"
        }), 404
    try:
        cliente_deletado = ClienteSchema.model_validate(cliente).model_dump()
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Cliente deletado com sucesso",
            "data": cliente_deletado
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Erro ao deletar cliente",
            "error": str(e)
        }), 500
