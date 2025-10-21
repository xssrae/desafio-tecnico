import pytest
import os
import tempfile
from app import create_app, db
from app.db_models import ClienteDB
from app import TestConfig

@pytest.fixture(scope='module')
def test_app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(config_class=TestConfig)
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "WTF_CSRF_ENABLED": False 
    })

    with app.app_context():
        pass 
    
    yield app
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture(scope='module')
def test_client(test_app):
    return test_app.test_client()

@pytest.fixture(scope='function')
def init_database(test_app):
    with test_app.app_context():
        db.create_all()

        c1 = ClienteDB(
            cpf="111", 
            nome="Joao da Silva", 
            email="joao@test.com",
            telefone="111111",
            agencia="0001", 
            conta="1", 
            tipo_conta="C", 
            cartao_debito="1"
        )
        c2 = ClienteDB(
            cpf="222", 
            nome="Maria Silva", 
            email="maria@test.com", 
            telefone="222222",
            agencia="0001", 
            conta="2", 
            tipo_conta="C", 
            cartao_debito="2"
        )
        c3 = ClienteDB(
            cpf="333", 
            nome="Roberto Carlos", 
            email="roberto@test.com",
            telefone="333333",
            agencia="0001", 
            conta="3", 
            tipo_conta="C", 
            cartao_debito="3"
        )
        
        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)
        db.session.commit()

        yield db 

        db.session.remove()
        db.drop_all()

def test_listar_todos_clientes(test_client, init_database): # GET - Listar todos
    response = test_client.get("/clientes/")
    
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] == True
    assert len(json_data["data"]) == 3

def test_buscar_cliente_por_nome_sucesso(test_client, init_database):  # GET - Buscar por nome
    response = test_client.get("/clientes/?nome=Silva")
    
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] == True
    assert len(json_data["data"]) == 2
    assert json_data["data"][0]["nome"] == "Joao da Silva"

def test_buscar_cliente_por_nome_case_insensitive(test_client, init_database):  # GET - Buscar por nome case insensitive
    response = test_client.get("/clientes/?nome=roberto")
    
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] == True
    assert len(json_data["data"]) == 1
    assert json_data["data"][0]["nome"] == "Roberto Carlos"

def test_buscar_cliente_nao_encontrado(test_client, init_database): # GET - Cliente não encontrado
    response = test_client.get("/clientes/?nome=Paula")
    
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["success"] == False
    assert "Nenhum cliente encontrado" in json_data["message"]

def  test_adicionar_cliente_sucesso(test_client, init_database): # POST - Sucesso
    new_cliente = {
        "cpf": "444",
        "nome": "Ana Paula",
        "email": "ana@test.com",
        "telefone": "444444",
        "agencia": "0001",
        "conta": "4",
        "tipo_conta": "C",
        "cartao_debito": "4"
    }
    response = test_client.post("/clientes/", json=new_cliente)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["success"] == True
    assert json_data["data"]["nome"] == "Ana Paula"
    assert json_data["data"]["cpf"] == "444"
    assert json_data["data"]["email"] == "ana@test.com"
    assert json_data["data"]["telefone"] == "444444"
    assert json_data["data"]["agencia"] == "0001"
    assert json_data["data"]["conta"] == "4"
    assert json_data["data"]["tipo_conta"] == "C"
    assert json_data["data"]["cartao_debito"] == "4"

def test_adicionar_cliente_cpf_duplicado(test_client, init_database): # POST - CPF duplicado
    new_cliente = {
        "cpf": "111",
        "nome": "Pedro Alves",
        "email": "pedro@test.com",
        "telefone": "666666",
        "agencia": "0001",
        "conta": "6",
        "tipo_conta": "C",
        "cartao_debito": "6"
    }
    response = test_client.post("/clientes/", json=new_cliente)
    assert response.status_code == 409
    json_data = response.get_json()
    assert json_data["success"] == False
    assert "CPF já cadastrado" in json_data["message"]

def test_adicionar_cliente_cpf_valor_vazio(test_client, init_database): # POST - CPF ausente
    new_cliente = {
        "nome": "Carlos Eduardo",
        "email": "carlos@test.com",
        "cpf": "",
        "telefone": "555555",
        "agencia": "0001",
        "conta": "5",
        "tipo_conta": "C",
        "cartao_debito": "5"
    }
    response = test_client.post("/clientes/", json=new_cliente)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["success"] == False
    assert "Dados inválidos" in json_data["message"]

def test_adicionar_cliente_campo_email_vazio(test_client, init_database):    # POST - Email vazio
    new_cliente = {
        "cpf": "666",
        "nome": "Lucas Mendes",
        "email": "",
        "telefone": "00000000",
        "agencia": "0001",
        "conta": "8",
        "tipo_conta": "C",
        "cartao_debito": "8"
    }
    response = test_client.post("/clientes/", json=new_cliente)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["success"] == False
    assert "Dados inválidos" in json_data["message"]

def test_atualizar_cliente_sucesso(test_client, init_database): # PUT - Sucesso
    updated_data = {
        "cpf": "111", 
        "nome": "Joao Pereira",
        "email": "joao.pereira@test.com", 
        "telefone": "999999",
        "agencia": "0002",
        "conta": "10",
        "tipo_conta": "C",
        "cartao_debito": "10"
    }
    response = test_client.put("/clientes/111", json=updated_data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] == True
    assert json_data["data"]["nome"] == "Joao Pereira"
    assert json_data["data"]["email"] == "joao.pereira@test.com" 
    assert json_data["data"]["telefone"] == "999999"
    assert json_data["data"]["agencia"] == "0002"
    assert json_data["data"]["conta"] == "10"
    assert json_data["data"]["tipo_conta"] == "C"
    assert json_data["data"]["cartao_debito"] == "10"

def test_atualizar_cliente_nao_encontrado(test_client, init_database):  # PUT - Cliente não encontrado
    updated_data = {
        "cpf": "999", 
        "nome": "Carlos Souza",
        "email": "carlos@souza.com",
        "telefone": "888888",
        "agencia": "0003",
        "conta": "11",
        "tipo_conta": "C",
        "cartao_debito": "11"
    }
    response = test_client.put("/clientes/999", json=updated_data)
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["success"] == False
    assert "Cliente não encontrado" in json_data["message"]

def test_atualizar_cliente_campo_nome_vazio(test_client, init_database): # PUT - Nome vazio
    updated_data = {
        "cpf": "222", 
        "email": "beltrano@test.com", 
        "nome": "", 
        "telefone": "777777",
        "agencia": "0004",
        "conta": "12",
        "tipo_conta": "C",
        "cartao_debito": "12"
    }
    response = test_client.put("/clientes/222", json=updated_data)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["success"] == False
    assert "Dados inválidos" in json_data["message"]

def test_atualizar_cliente_campo_email_vazio(test_client, init_database):    # PUT - Email vazio
    updated_data = {
        "cpf": "333", 
        "nome": "Maria Oliveira",
        "email": "", 
        "telefone": "888888",
        "agencia": "0005",
        "conta": "13",
        "tipo_conta": "C",
        "cartao_debito": "13"
    }
    response = test_client.put("/clientes/333", json=updated_data)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["success"] == False
    assert "Dados inválidos" in json_data["message"]

def test_deletar_cliente_sucesso(test_client, init_database): # DELETE - Sucesso
    response = test_client.delete("/clientes/1") 
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] == True
    assert "Cliente deletado com sucesso" in json_data["message"]
    assert json_data["data"]["cpf"] == "111" # Verificar se é o cliente certo
    assert json_data["data"]["nome"] == "Joao da Silva"


def test_deletar_cliente_nao_encontrado(test_client, init_database):  # DELETE - Cliente não encontrado
    response = test_client.delete("/clientes/999") 
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["success"] == False
    assert "Cliente não encontrado" in json_data["message"]