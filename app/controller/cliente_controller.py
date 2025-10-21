from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app import db
from app.db_models import ClienteDB
from app.model.cliente_model import ClienteCreate, ClienteUpdate, Cliente as ClienteSchema

cliente_bp = Blueprint("clientes", __name__, url_prefix="/clientes")

@cliente_bp.route("/", methods=["GET"]) # GET - Listar todos ou buscar por nome (Obrigatório)
def buscar_ou_listar_clientes():
    """
    Listar todos os clientes ou buscar por nome
    Este endpoint permite listar todos os clientes cadastrados ou
    filtrar aqueles que contêm uma string no nome.
    ---
    tags:
      - Clientes
    parameters:
      - name: nome
        in: query
        type: string
        required: false
        description: Nome ou parte do nome do cliente para buscar
    responses:
      200:
        description: Lista de clientes encontrados
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            data:
              type: array
              items:
                $ref: '#/definitions/Cliente'
      404:
        description: Nenhum cliente encontrado (apenas ao buscar por nome)
      500:
        description: Erro interno do servidor
    """
    try:
        nome = request.args.get('nome')

        if nome:
            clientes_db = ClienteDB.query.filter(
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


@cliente_bp.route("/<int:id>", methods=["GET"]) # Adicional - Endpoint to get client by ID
def buscar_cliente_por_id(id: int):
    """
    Buscar cliente por ID
    Retorna os dados de um cliente específico baseado no seu ID.
    ---
    tags:
      - Clientes
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID único do cliente
    responses:
      200:
        description: Cliente encontrado com sucesso
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            data:
              $ref: '#/definitions/Cliente'
      404:
        description: Cliente não encontrado
      500:
        description: Erro interno do servidor
    """
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


@cliente_bp.route("/", methods=["POST"])
def criar_cliente():
    """
    Criar um novo cliente
    Endpoint para cadastrar um novo cliente na base de dados.
    O CPF e o Email devem ser únicos.
    ---
    tags:
      - Clientes
    parameters:
      - name: body
        in: body
        required: true
        description: Dados do cliente para criação
        schema:
          $ref: '#/definitions/ClienteCreate'
    responses:
      201:
        description: Cliente criado com sucesso
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            data:
              $ref: '#/definitions/Cliente'
      400:
        description: Requisição inválida ou dados inválidos (JSON ou Pydantic)
      409:
        description: Conflito (CPF ou Email já cadastrado)
      500:
        description: Erro interno do servidor
    """
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
    
    # ----- REMOVIDO -----
    # Pydantic agora valida TUDO
    # if not cliente_create.email: ...
    # if not cliente_create.cpf: ..

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
            # CORREÇÃO (Modernização Pydantic)
            "data": ClienteSchema.model_validate(novo_cliente).model_dump()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Erro ao salvar cliente",
            "error": str(e)
        }), 500


@cliente_bp.route("/<string:cpf>", methods=["PUT"])
def atualizar_cliente(cpf: str):
    """
    Atualizar um cliente existente
    Permite atualizar o nome e/ou email de um cliente existente, 
    identificado pelo seu CPF.
    ---
    tags:
      - Clientes
    parameters:
      - name: cpf
        in: path
        type: string
        required: true
        description: CPF do cliente a ser atualizado
      - name: body
        in: body
        required: true
        description: Dados do cliente para atualização
        schema:
          $ref: '#/definitions/ClienteUpdate'
    responses:
      200:
        description: Cliente atualizado com sucesso
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            data:
              $ref: '#/definitions/Cliente'
      400:
        description: Requisição inválida ou dados inválidos (JSON ou Pydantic)
      404:
        description: Cliente não encontrado com o CPF informado
      409:
        description: Conflito (Email já cadastrado por outro usuário)
      500:
        description: Erro interno do servidor
    """
    cliente_db = ClienteDB.query.filter_by(cpf=cpf).first()

    if cliente_db is None:
        return jsonify({
            "success": False,
            "message": "Cliente não encontrado",
            "error": f"Nenhum cliente encontrado com CPF informado"
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
            "message": "Dados inválidos",
            "errors": e.errors()
        }), 400

    if "nome" in data and (cliente_update.nome is None or str(cliente_update.nome).strip() == ""):
        return jsonify({
            "success": False,
            "message": "Campo 'nome' não pode ser vazio",
            "error": "O campo 'nome' não pode ser vazio"
        }), 400

    if "email" in data and (cliente_update.email is None or str(cliente_update.email).strip() == ""):
        return jsonify({
            "success": False,
            "message": "Campo 'email' não pode ser vazio",
            "error": "O campo 'email' não pode ser vazio"
        }), 400

    try:
        if cliente_update.email is not None:
            email_existente = ClienteDB.query.filter(
                ClienteDB.email == cliente_update.email, 
                ClienteDB.id != cliente_db.id # <-- CORRIGIDO
            ).first() 

            if email_existente:
                return jsonify({
                    "success": False,
                    "message": "Email já cadastrado",
                    "error": f"O email '{cliente_update.email}' já está cadastrado"
                }), 409    
        if cliente_update.cpf is not None:
            cpf_existente = ClienteDB.query.filter(
                ClienteDB.cpf == cliente_update.cpf, 
                ClienteDB.id != cliente_db.id
            ).first()
            if cpf_existente:
                return jsonify({
                    "success": False,
                    "error": f"O CPF inserido já está cadastrado"
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
        return jsonify({
            "success": False,
            "message": "Erro ao atualizar cliente",
            "error": str(e)
        }), 500

@cliente_bp.route("/<int:id>", methods=["DELETE"])
def deletar_cliente(id: int):

    """
    Deletar um cliente
    Remove um cliente da base de dados, identificado pelo ID.
    ---
    tags:
      - Clientes
    parameters:
      - name: cpf
        in: path
        type: string
        required: true
        description: ID do cliente a ser deletado
    responses:
      200:
        description: Cliente deletado com sucesso
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            data:
              $ref: '#/definitions/Cliente'
      404:
        description: Cliente não encontrado com o ID informado
      500:
        description: Erro interno do servidor
    """

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
