import requests
from hmac_helper import *

chave = get_chave()
url = "http://127.0.0.1:8000/"

try:
    response = requests.get(url, timeout=5)

    response.raise_for_status()

    dados = response.json()

    # simular ataque de replay
    # espera um tempo antes de validar
    # time.sleep(30)

    if mensagem_eh_valida(dados, chave):

        if mensagem_eh_recente(dados):
            print("Tudo OK!!!")
        else:
            print("Mensagem expirada")

    else:
        print("HMAC inválido")

except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")

except ValueError:
    print("Resposta não contém JSON válido")