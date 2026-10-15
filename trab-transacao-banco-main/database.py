from chaves import gerar_par_de_chaves
import json


estado_inicial = {
    "usuarios": [],
    "transacaoes": []
}

def ler_banco(leitura=None) -> dict:
    with open('banco.json', 'r') as file:
        try:
            dados = file.read()
            if leitura == 5:
                print("banco antes da transacao:")
                print(dados)
            banco = json.loads(dados)
            print('========= print banco =========')
            return banco
        except Exception as e:
            print(f"Erro ao ler o banco: {e}")
            return estado_inicial
    
def get_usuarios() -> list:
    banco = ler_banco()
    return banco["usuarios"]

def usuario_existe(nome: str) -> tuple[bool, int]:
    usuarios = get_usuarios()
    for i, u in enumerate(usuarios):
        if u["nome"].lower() == nome.lower():
            return True, i
    return False, -1

def consultar_saldo(nome: str) -> float:
    usuarios = get_usuarios()
    for u in usuarios:
        if u["nome"].lower() == nome.lower():
            return u["saldo"]
    return 0.0

def consultar_chave_publica(nome: str) -> str:
    usuarios = get_usuarios()
    for u in usuarios:
        if u["nome"].lower() == nome.lower():
            return u["chave_publica"]
    return ""

def consultar_chave_privada(nome: str) -> str:
    usuarios = get_usuarios()
    for u in usuarios:
        if u["nome"].lower() == nome.lower():
            return u["chave_privada"]
    return ""

def aplicar_transacao(remetente: str, destinatario: str, valor: float) -> bool:
    
    banco = ler_banco(5)
        
    with open('banco.json', 'w') as file:
        
        contador = 0
        for u in banco["usuarios"]:
            if u["nome"].lower() == remetente.lower():
                u["saldo"] -= valor
                print("Valor H:", u["saldo"])
                contador += 1
            elif u["nome"].lower() == destinatario.lower():
                u["saldo"] += valor
                print("Valor G:", u["saldo"])
                contador += 1
            
            if contador == 2:
                break
            
        try:
            json.dump(banco, file, indent=4, ensure_ascii=False)
            return True
        
        except:
            return False

def salvar_usuario(data: dict) -> bool:
    
    banco = ler_banco()
    
    with open('banco.json', 'w') as file:
        
        data["saldo"] = 1000
        
        try: 
            data["chave_publica"], data["chave_privada"] = gerar_par_de_chaves()

            banco["usuarios"].append(data)

            json.dump(banco, file, indent=4, ensure_ascii=False)
            
            return True
        except Exception as e: 
            print(f"Erro ao salvar usuário: {e}")
            return False
