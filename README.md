# API de Cadastro de Clientes

API simples desenvolvida como parte de um **teste técnico para a posição de Analista de Engenharia de TI Júnior**.
A aplicação permite **cadastrar, listar e consultar clientes**, com persistência de dados em um banco de dados **PostgreSQL**.

---

## ⚙️ Tecnologias Utilizadas

* **Linguagem:** Python 3.9+
* **Framework:** Flask
* **Banco de Dados:** PostgreSQL (executado via Docker)
* **ORM:** SQLAlchemy (ou Flask-SQLAlchemy)
* **Documentação:** Flasgger (Swagger UI)
* **Testes:** Pytest

---

## 📦 Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:

* **Python 3.9+**
* **Docker** (e Docker Compose)

---

## 🚀 Como Executar o Projeto

### 1. **Clone o repositório:**

```bash
git clone https://github.com/xssrae/desafio-tecnico
cd api-clientes
```

### 2. **Crie e ative um ambiente virtual:**

- Mac ou Linux
```bash
# Cria o ambiente virtual
python -m venv venv

# Ativa o ambiente
.\venv\Scripts\Activate
```

- Windows
```powershell
# Cria o ambiente virtual
python -m venv venv
# Ativa o ambiente
.\venv\Scripts\Activate
```
  > ⚠️ Atenção: Caso renomeie a pasta do projeto, exclua e recrie o venv após a mudança. Ambientes virtuais quebram quando a pasta raiz é renomeada.

### 3. Crie o arquivo de configuração `.env`

Crie um arquivo chamado .env na raiz do projeto e adicione o seguinte conteúdo:

```ini
# ==================================
# Configuração do Docker (para criar o banco)
# ==================================
POSTGRES_USER={USER}
POSTGRES_PASSWORD={SENHA}
POSTGRES_DB=clientes_db

# ==================================
# Configuração do Flask (para conexão com o DB)
# ==================================
DATABASE_URL="postgresql://admin:9928@localhost:5433/clientes_db"

# ==================================
# Configuração do Servidor Flask
# ==================================
FLASK_APP=run.py
FLASK_DEBUG=1
FLASK_RUN_PORT=5000
FLASK_RUN_HOST=0.0.0.0
```

### 4. **Instale as dependências:**

```bash
# (Opcional) Atualize o pip
python -m pip install --upgrade pip

# Instale as dependências do projeto
pip install -r requirements.txt
```

### 5. **Inicie o container do banco de dados com o Docker Compose:**

```bash
docker-compose up -d
```

### 6. Aplique as migrações do banco de dados:

Com o container do PostgreSQL em execução, crie as tabelas do banco com o Flask-Migrate:
```bash
# Inicializa a pasta de migrações (somente na primeira vez)
flask db init

# Cria as tabelas
flask db upgrade
```
Caso altere os modelos, gere uma nova migração com:
```bash
flask db migrate -m "Descrição da migração"
```

### 7. Execute a aplicação Flask:

```bash
flask run
```

### A API estará disponível em:
👉 `http://127.0.0.1:5000`

### A documentação interativa (Swagger UI via Flasgger) estará em:
👉 `http://127.0.0.1:5000/apidocs/`

---

## 🧪 Executando os Testes

Com o ambiente configurado e as dependências instaladas, execute o comando abaixo na raiz do projeto:

```bash
pytest
```
---

## 📚 Documentação dos Endpoints

### 1. Cadastrar Cliente

* **Método:** `POST`
* **Endpoint:** `/clientes/`
* **Descrição:** Cria um novo cliente.

#### Corpo da Requisição (Exemplo)

```json
{
  "nome": "Fulano de Tal",
  "email": "fulano.tal@example.com",
  "telefone": "11987654321"
}
```

#### Resposta de Sucesso (201 Created)

```json
{
  "id": 1,
  "nome": "Fulano de Tal",
  "email": "fulano.tal@example.com",
  "telefone": "11987654321"
}
```

---

### 2. Listar Todos os Clientes

* **Método:** `GET`
* **Endpoint:** `/clientes/`
* **Descrição:** Retorna uma lista com todos os clientes cadastrados.

#### (Desafio Extra) Filtrar por nome:

`GET /clientes/?nome=fulano`

#### Resposta de Sucesso (200 OK)

```json
[
  {
    "id": 1,
    "nome": "Fulano de Tal",
    "email": "fulano.tal@example.com",
    "telefone": "11987654321"
  }
]
```

---

### 3. Consultar Cliente por ID

* **Método:** `GET`
* **Endpoint:** `/clientes/<int:id>`
* **Descrição:** Retorna os dados de um cliente específico.
* **Exemplo de URL:** `http://127.0.0.1:5000/clientes/1`

#### Resposta de Sucesso (200 OK)

```json
{
  "id": 1,
  "nome": "Fulano de Tal",
  "email": "fulano.tal@example.com",
  "telefone": "11987654321"
}
```

#### Resposta de Erro (404 Not Found)

```json
{
  "error": "Cliente não encontrado."
}
```

---

## 💻 Exemplos de Requisições com `curl`

A seguir estão exemplos práticos para testar os endpoints diretamente pelo terminal:

### 🔸 1. Criar um novo cliente

```bash
curl -X POST http://127.0.0.1:5000/clientes/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Fulano de Tal",
    "email": "fulano.tal@example.com",
    "telefone": "11987654321"
  }'
```

### 🔸 2. Listar todos os clientes

```bash
curl -X GET http://127.0.0.1:5000/clientes/
```

### 🔸 3. Buscar cliente por ID

```bash
curl -X GET http://127.0.0.1:5000/clientes/1
```

### 🔸 4. Buscar cliente por nome (parâmetro de consulta)

```bash
curl -X GET "http://127.0.0.1:5000/clientes/?nome=fulano"
```

---
## Solução de Problemas (Troubleshooting)
Para entender como resolver possíveis problemas, leia o arquivo:

- [Troubleshooting](https://github.com/xssrae/desafio-tecnico/blob/main/TROUBLESHOOTING.md) 🛠️
---

## 🔮 Melhorias Futuras (Roadmap)

* ✅ **Validação de Schemas:** Implementar validação dos dados de entrada (ex.: com Pydantic ou Marshmallow) para garantir a integridade dos payloads recebidos.
* ✅ **Serialização de Saída:** Adicionar serialização de saída utilizando a mesma biblioteca de schema, garantindo consistência nas respostas da API.
* ✅ **Tratamento Centralizado de Erros:** Criar um manipulador global de erros no Flask para padronizar respostas de erro (ex.: 404, 400, 500).
* ✅ **Documentação Detalhada:** Melhorar a documentação no Flasgger (Swagger), incluindo schemas de entrada e saída, códigos de status e descrições completas para cada endpoint.
