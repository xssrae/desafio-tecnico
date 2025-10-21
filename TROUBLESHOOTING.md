# 🛠️ Solução de Problemas (Troubleshooting)

Aqui estão alguns erros comuns e como resolvê-los:

---

## ⚠️ `flask: comando não reconhecido`

**Causa 1:** O ambiente virtual não está ativo.  
➡️ **Solução:** Execute `.env\Scripts\Activate` (Windows) ou `source venv/bin/activate` (Linux/Mac).

**Causa 2:** O `venv` foi corrompido (geralmente após renomear a pasta).  
➡️ **Solução:** Exclua o `venv`, recrie-o e reinstale as dependências.

---

## ⚠️ `ModuleNotFoundError: No module named 'pydantic'` ou `'email_validator'`

**Causa:** Dependência ausente.  
➡️ **Solução:** Instale manualmente:
```bash
pip install pydantic 'pydantic[email]'
```
Em seguida, atualize o `requirements.txt`:
```bash
pip freeze > requirements.txt
```

---

## ⚠️ Erro Docker: `Container name ".../postgres_db_clientes" is already in use`

**Causa:** Um container antigo ainda está ativo.  
➡️ **Solução:**  
- Preferencial: `docker-compose down`  
- Alternativa: `docker rm -f postgres_db_clientes`

---

## ⚠️ Erro Docker: `The "POSTGRES_USER" variable is not set`

**Causa:** O Docker Compose não encontrou o arquivo `.env`.  
➡️ **Solução:**  
Verifique se o arquivo se chama exatamente `.env` (sem extensão).  
Depois, recrie o container:
```bash
docker-compose down
docker-compose up -d --force-recreate
```

---

## ⚠️ Erro Flask: `OperationalError: connection to server at "localhost" (::1), port 5432 failed`

**Causa:** A `DATABASE_URL` está incorreta.  
➡️ **Solução:**  
Confirme que está usando a **porta externa** (`5433`) e a senha corretas no `.env`.
