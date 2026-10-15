from fastapi import FastAPI
from hmac_helper import *
import time

app = FastAPI()

@app.get("/")
def index():
    
    # simular dados da estacao
    timestamp = int(time.time())
    dados = {
        "temperatura": 25,
        "umidade": 70,
        "pressao": 1013,
        "timestamp": timestamp
    }

    chave = get_chave()
    mensagem_autenticada = criar_mensagem_autenticada(dados, chave)

    return mensagem_autenticada

