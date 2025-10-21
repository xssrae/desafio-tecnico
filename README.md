# 🧩 API de Cadastro de Clientes

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

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/xssrae/desafio-tecnico-itau
   cd api-clientes
   ```

2. **(Opcional, mas recomendado) Crie e ative um ambiente virtual:**

  - Mac ou Linux
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
   
  - Windows
   ```bash
   python -m venv venv
   .venv\Scripts\activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Inicie o container do banco de dados com o Docker Compose:**

   ```bash
   docker-compose up -d
   ```

5. **Crie um arquivo `.env` na raiz do projeto** com o conteúdo abaixo, configurando a conexão com o banco:

   ```ini
   DATABASE_URL="postgresql://admin:admin@localhost:5432/clientes_db"
   ```

6. **Defina as variáveis de ambiente do Flask**
   (assumindo que o arquivo principal seja `app.py` ou `main.py`):

   * **Linux/macOS:**

     ```bash
     export FLASK_APP=app.main
     export FLASK_ENV=development  # (Opcional)
     ```

   * **Windows (CMD):**

     ```bash
     set FLASK_APP=app.main
     set FLASK_ENV=development
     ```

7. **Execute a aplicação:**

   ```bash
   flask run --reload
   ```

8. A API estará disponível em:
   👉 `http://127.0.0.1:5000`

9. A documentação interativa (Swagger UI via Flasgger) estará em:
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

## 🔮 Melhorias Futuras (Roadmap)

* ✅ **Validação de Schemas:** Implementar validação dos dados de entrada (ex.: com Pydantic ou Marshmallow) para garantir a integridade dos payloads recebidos.
* ✅ **Serialização de Saída:** Adicionar serialização de saída utilizando a mesma biblioteca de schema, garantindo consistência nas respostas da API.
* ✅ **Tratamento Centralizado de Erros:** Criar um manipulador global de erros no Flask para padronizar respostas de erro (ex.: 404, 400, 500).
* ✅ **Documentação Detalhada:** Melhorar a documentação no Flasgger (Swagger), incluindo schemas de entrada e saída, códigos de status e descrições completas para cada endpoint.
