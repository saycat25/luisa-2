#!/bin/bash

echo "🚀 Implantando Luísa Monteiro no Campos Cloud..."

# Verificar dependências
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado!"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não encontrado!"
    exit 1
fi

# Criar diretórios necessários
echo "📁 Criando estrutura de diretórios..."
mkdir -p ./lu_memory ./projects ./audio
chmod -R 755 ./lu_memory ./projects ./audio

# Verificar arquivo .env
if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado, copiando de .env.example..."
    cp .env.example .env
    echo "📝 Por favor, configure as variáveis no arquivo .env antes de continuar!"
    exit 1
fi

# Build e deploy
echo "🐳 Construindo e iniciando containers..."
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Aguardar inicialização
echo "⏳ Aguardando inicialização..."
sleep 30

# Verificar status
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Luísa Monteiro implantada com sucesso!"
    echo "🔗 Health Check: http://localhost:8000/health"
    echo "📊 Logs: docker-compose logs -f luisa-digital"
else
    echo "❌ Erro na implantação. Verifique os logs:"
    docker-compose logs luisa-digital
    exit 1
fi
