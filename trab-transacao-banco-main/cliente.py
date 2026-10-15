import requests
import json
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import chaves
url = 'http://localhost:8000'

dados = {
    'remetente': 'Gustavo',
    'destinatario': 'Henrique',
    'valor': 700.0
}


chave_privada_str = "-----BEGIN PRIVATE KEY-----\n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\nO5pQ+hMxuTVcQl37zmoUsdQy\n-----END PRIVATE KEY-----\n"
pv_key = chaves.deserializar_chaves(private_key=chave_privada_str)


# Configuração do esquema de preenchimento (padding)
# Usando PSS (Probabilistic Signature Scheme) com MGF1 e SHA-256
padding_config = padding.PSS(
                              mgf=padding.MGF1(hashes.SHA256()),
                              salt_length=padding.PSS.MAX_LENGTH
                            )
dados_em_bytes = json.dumps(dados, sort_keys=True, separators=(",", ":")).encode('utf-8')
# Assinatura da mensagem usando a chave privada de Bob, com a configuração de padding e SHA-256
signature = pv_key.sign(
                              dados_em_bytes,
                              padding_config,
                              hashes.SHA256() # A função hash utilizada para gerar o resumo da mensagem
                            )

# Criação de um dicionário com a mensagem e a assinatura

dados['assinatura'] = signature.hex()

response = requests.post(f'{url}/realizar-transacao', json=dados)

response.raise_for_status()

response_data = response.json()

print(response_data)

