from pydantic import BaseModel, EmailStr, ConfigDict, constr
from typing import Optional

class ClienteCreate(BaseModel):
    """
    Modelo para criação de cliente.
    cpf, nome, e email são obrigatórios.
    constr(min_length=1) garante que a string não pode ser vazia.
    """
    cpf: constr(strip_whitespace=True, min_length=1)
    nome: constr(strip_whitespace=True, min_length=1)
    email: EmailStr 
    
    # Campos opcionais
    telefone: str = None
    agencia: str = None
    conta: str = None
    tipo_conta: str = None
    cartao_debito: str = None
    cartao_credito: Optional[str] = None
    bandeira_cartao_credito: Optional[str] = None

class Cliente(BaseModel):
    """
    Modelo para serialização de saída (respostas da API).
    """
    id: int
    cpf: str = None
    nome: str
    email: EmailStr = None
    telefone: str = None
    agencia: str = None
    conta: str = None
    tipo_conta: str = None
    cartao_debito: str = None
    cartao_credito: Optional[str] = None
    bandeira_cartao_credito: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class ClienteUpdate(BaseModel):
    cpf: constr(strip_whitespace=True, min_length=1)
    nome: constr(strip_whitespace=True, min_length=1)
    email: EmailStr
    
    # Campos opcionais
    telefone: Optional[str] = None
    agencia: Optional[str] = None
    conta: Optional[str] = None
    tipo_conta: Optional[str] = None
    cartao_debito: Optional[str] = None
    cartao_credito: Optional[str] = None
    bandeira_cartao_credito: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)