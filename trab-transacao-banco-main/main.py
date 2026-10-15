from fastapi import FastAPI
from models import UsuarioDataReq, TransacaoDataReq
import database
import chaves
from datetime import datetime
import time


app = FastAPI()

sessao = {}

historico_logs = []

@app.get("/")
def index():
    return {"message": "API on"}


@app.post("/cadastro")
def cadastrar_usuario(user: UsuarioDataReq):
    
    data = user.model_dump()
    
    usuario_existe = database.usuario_existe(data["nome"])[0]
        
    if usuario_existe:
        return {
            "erro": "Usuário já cadastrado!!!"
        }
    
    usuario_salvo = database.salvar_usuario(data)

    if usuario_salvo:
        return {"message": f"Usuario '{data['nome']}' cadastrado!!!"}
    return {"erro": "Erro ao cadastrar usuário!!!"}


@app.post("/login")
def login(user: UsuarioDataReq):

    data = user.model_dump()
    usuarios = database.get_usuarios()
    
    usuario_existe, idx_user = database.usuario_existe(data["nome"])
        
    if not usuario_existe:
        return {
            "erro": "Usuário não cadastrado!!!"
        }

    senha_correta = usuarios[idx_user]["senha"] == data["senha"]

    if not senha_correta:
        return {
            "erro": "Senha incorreta!!!"
        }

    
    sessao["usuario"] = usuarios[idx_user]
    
    return {"message": f"Usuario '{data['nome']}' logado!!!"}


@app.get("/usuario-logado")
def usuario_logado():

    if not sessao:
        return {
            "erro": "Nenhum usuário logado!!!"
        }
    
    return {
        "usuario": sessao["usuario"]["nome"]
    }


@app.post("/realizar-transacao")
def realizar_transacao(transacao: TransacaoDataReq):

    ##Verificar se está logado
    if not sessao:
        return {
            "erro": "Nenhum usuário logado!!!"
        }
        
    print('====== realizar-transacao =======')
    print(sessao)

    data = transacao.model_dump()
    remetente = data["remetente"]
    destinatario = data["destinatario"]
    valor = data["valor"]
    assinatura = data["assinatura"]
    
    remetente_existe = database.usuario_existe(remetente)[0]
    destinatario_existe = database.usuario_existe(destinatario)[0]
    usuarios_existe = remetente_existe and destinatario_existe

    print(remetente_existe, destinatario_existe, usuarios_existe)

    if not usuarios_existe:
        return {
            "erro": "Remetente ou destinatário não cadastrado!!!"
        }

    consultar_saldo = database.consultar_saldo(remetente)

    if consultar_saldo < valor and valor > 0:
        return {
            "erro": "Saldo insuficiente!!!"
        }

    if sessao["usuario"]["nome"].lower() != remetente.lower():
        return {
            "erro": "Usuário logado não é o remetente da transação!!!"
        }
    
    assinatura_valida = chaves.validar_assinatura(remetente, data)
    
    if not assinatura_valida:
        return {
            "erro": "Assinatura inválida!!!"
        }
    
    transacao_aplicada = database.aplicar_transacao(remetente, destinatario, valor) 

    if transacao_aplicada:
        registrar_log(remetente, destinatario, valor, assinatura, True)
        return {"message": f"Transação realizada com sucesso entre '{remetente}' e '{destinatario}'!"}
    
    registrar_log(remetente, destinatario, valor, assinatura, False)
    
    return {"erro": "Erro ao realizar transação!!!"}


def registrar_log(remetente, destinatario, valor, assinatura, deu_sucesso):
    historico_logs.append({
        "remetente": remetente,
        "destinatario": destinatario,
        "valor": valor,
        "assinatura": assinatura,
        "timestamp": datetime.fromtimestamp(time.time()).strftime('%d/%m/%Y %H:%M:%S'),
        "status": "Sucesso" if deu_sucesso else "Falha",
    })


@app.get("/logs")
def logs():
    return historico_logs