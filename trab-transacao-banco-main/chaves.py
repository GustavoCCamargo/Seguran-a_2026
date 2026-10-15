from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import json
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature



def gerar_par_de_chaves() -> tuple[str, str]:
  """
  Gerar par de chaves pública e privada

  :return: par de cahves (chave pública, chave privada)
  """
  pv_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=3072,
    backend=default_backend()
  )
  pb_key = pv_key.public_key()

  private_bytes = pv_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(), )

  public_bytes = pb_key.public_bytes(
          encoding=serialization.Encoding.PEM,
          format=serialization.PublicFormat.SubjectPublicKeyInfo, )

  pb_str_key = public_bytes.decode('utf-8')
  pv_str_key = private_bytes.decode('utf-8')

  return pb_str_key, pv_str_key


def deserializar_chaves(
    par_chaves: tuple[str, str] | None = None,
    private_key: str | None = None,
    public_key: str | None = None
):

  if private_key is not None:
    return serialization.load_pem_private_key(
      private_key.encode(),
      password=None,
      backend=default_backend()
  )
    
  if public_key is not None:
      return serialization.load_pem_public_key(
      public_key.encode(),
      backend=default_backend()
  )
    
  if par_chaves is not None:
    pb_str_key, pv_str_key = par_chaves

    loaded_private_key = serialization.load_pem_private_key(
        pv_str_key.encode(),
        password=None,
        backend=default_backend()
    )

    loaded_public_key = serialization.load_pem_public_key(
        pb_str_key.encode(),
        backend=default_backend()
    )
    
    return loaded_public_key, loaded_private_key
  
  return ValueError("Você deve fornecer pelo menos um dos parâmetros: par_chaves, private_key ou public_key.")


def assinar_dados(chave: str, dados: bytes):
  
  pv_key = deserializar_chaves(private_key=chave)

  # Configuração do esquema de preenchimento (padding)
  # Usando PSS (Probabilistic Signature Scheme) com MGF1 e SHA-256
  padding_config = padding.PSS(
    mgf=padding.MGF1(hashes.SHA256()),
    salt_length=padding.PSS.MAX_LENGTH
  )
  dados_em_bytes = json.dumps(dados, sort_keys=True).encode('utf-8')
  
  # Assinatura da mensagem usando a chave privada de Bob, com a configuração de padding e SHA-256
  signature = pv_key.sign(
    dados_em_bytes,
    padding_config,
    hashes.SHA256() # A função hash utilizada para gerar o resumo da mensagem
  )
  return signature.hex()


def validar_assinatura(
  remetente: str,
  pacote: dict
):
  
  import database
  
  remetente_pb_key = database.consultar_chave_publica(remetente)
  print('pb_key:', remetente_pb_key)
  pb_key = deserializar_chaves(public_key=remetente_pb_key)
  assinatura_recebida = pacote["assinatura"]
  del pacote['assinatura']
  
  assinatura_em_bytes = bytes.fromhex(assinatura_recebida)
  dados_em_bytes = json.dumps(pacote, sort_keys=True, separators=(',', ':')).encode('utf-8')
  
  print(f"[Debug Servidor] Bytes processados: {dados_em_bytes}")
  
  padding_config = padding.PSS(
                              mgf=padding.MGF1(hashes.SHA256()),
                              salt_length=padding.PSS.MAX_LENGTH
                            )
  
  try:
    pb_key.verify(
                          assinatura_em_bytes,      # A assinatura a ser verificada
                          dados_em_bytes,
                          padding_config, # Configuração de preenchimento PSS
                          hashes.SHA256() # A mesma função hash usada para assinar a mensagem
                        )
    
    return True
  
  except InvalidSignature:
    return False
