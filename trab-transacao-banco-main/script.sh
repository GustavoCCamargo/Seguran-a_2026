#!/bin/bash

echo "Configurando usuário..."
git config user.name "SeuNome"
git config user.email "seuemail@exemplo.com"

echo "Adicionando arquivos..."
git add .

# Verifica se há algo para commitar
if git diff-index --quiet HEAD --; then
    echo "Nenhuma alteração encontrada. Nada a commitar."
else
    # Pede para o usuário digitar a mensagem do commit
    read -p "Digite a mensagem do commit: " commit_message
    git commit -m "$commit_message"
fi

echo "Enviando para o repositório..."
git push
echo "Processo finalizado!"