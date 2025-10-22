from pydantic import BaseModel, EmailStr, ConfigDict, constr, field_validator
from typing import Optional

class ClienteCreate(BaseModel):
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

    @field_validator('email')
    @classmethod
    def check_email_not_empty_string(cls, v: str) -> str:
        
        if v == "":
            # Esta mensagem será incluída nos 'errors' do ValidationError
            raise ValueError("O campo 'email' não pode ser vazio")
        # Se não for vazio, permite que a validação EmailStr continue
        return v

class Cliente(BaseModel):
    id: int
    cpf: str 
    nome: str
    email: EmailStr
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