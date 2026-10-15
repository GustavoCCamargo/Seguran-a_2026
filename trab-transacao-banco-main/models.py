from pydantic import BaseModel


class UsuarioDataReq(BaseModel):
    nome: str
    senha: str
    

class TransacaoDataReq(BaseModel):
    remetente: str
    destinatario: str
    valor: float
    assinatura: str

