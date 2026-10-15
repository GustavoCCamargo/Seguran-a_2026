import hmac
import hashlib
import json
import os
import time
from dotenv import load_dotenv

# carregar variáveis de ambiente
load_dotenv()

# Função responsável por gerar o HMAC da mensagem
def gerar_hmac(dados, chave):

    # Converte os dados para texto JSON
    mensagem = json.dumps(dados, sort_keys=True)

    # Gera o HMAC utilizando SHA-256
    assinatura = hmac.new(
        chave.encode(),
        mensagem.encode(),
        hashlib.sha256
    ).hexdigest()

    return assinatura


# Função responsável por criar a mensagem autenticada
def criar_mensagem_autenticada(dados, chave):

    assinatura = gerar_hmac(dados, chave)

    mensagem_autenticada = {
        "dados": dados,
        "hmac": assinatura
    }

    return mensagem_autenticada


def mensagem_eh_recente(mensagem, tolerancia=2):

    timestamp = mensagem["dados"]["timestamp"]

    agora = int(time.time())

    return 0 <= (agora - timestamp) <= tolerancia


def mensagem_eh_valida(mensagem_recebida, chave):

    hmac_mensagem = mensagem_recebida["hmac"]
    
    hmac_gerado = gerar_hmac(mensagem_recebida["dados"], chave)

    return hmac.compare_digest(hmac_gerado, hmac_mensagem)


def get_chave():
    return os.getenv("SECRET_KEY")