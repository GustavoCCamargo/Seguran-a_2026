# Trabalho – Autenticação de Mensagens com HMAC

## Descrição
Desenvolvimento de uma estação meteorológica capaz de coletar dados climáticos, como temperatura, umidade e pressão atmosférica, e enviá-los a um servidor central. Para garantir a autenticidade e a integridade das informações transmitidas, a estação utiliza um **HMAC (Hash-based Message Authentication Code)** para assinar digitalmente cada mensagem antes do envio. Ao receber os dados, o servidor realiza a validação da assinatura HMAC utilizando uma chave secreta compartilhada, verificando se a mensagem foi realmente gerada pela estação meteorológica e se seu conteúdo não foi alterado durante a transmissão.


## Instalação

1. Clone o repositório
    ```bash
    git clone https://github.com/hick-hpe/trabalho-hmac.git
    cd trabalho-hmac
    ```

2. Crie e ative um ambiente virtual:
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Linux / Mac
    source venv/bin/activate
    ```

3. Instale as dependências:
    ```bash
    # Windows
    pip install -r requirements.txt

    # Linux / Mac
    pip3 install -r requirements.txt
    ```

4. Rode o servidor:
    ```bash
    uvicorn main:app --reload
    ```


Abra o navegador em [http://localhost:8000/](http://localhost:8000/) para testar.

