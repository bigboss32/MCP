#!/usr/bin/env bash
set -e

# --- 1. Verifica si uv está instalado ---
if ! command -v uv &> /dev/null; then
    echo "❌ 'uv' no está instalado."
    echo "Instálalo siguiendo estos pasos según tu sistema operativo:"
    unameOut="$(uname -s)"
    case "${unameOut}" in
        Linux*)
            echo "    curl -Ls https://astral.sh/uv/install.sh | sh"
            ;;
        Darwin*)
            echo "    brew install astral-sh/uv/uv"
            echo "  o"
            echo "    curl -Ls https://astral.sh/uv/install.sh | sh"
            ;;
        MINGW*|MSYS*)
            echo "    choco install uv"
            echo "  o"
            echo "    Descarga el instalador desde:"
            echo "    https://github.com/astral-sh/uv#installation"
            ;;
        *)
            echo "    Consulta https://github.com/astral-sh/uv#installation"
            ;;
    esac
    exit 1
fi

echo "✅ 'uv' está instalado."

# --- 2. Crea el entorno virtual si no existe ---
if [ ! -d ".venv" ]; then
    echo "🧪 Creando entorno virtual .venv con uv..."
    uv venv .venv
else
    echo "✅ El entorno virtual .venv ya existe."
fi

# --- 3. Activa el entorno virtual ---
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows Git Bash o similar
    source .venv/Scripts/activate
else
    # Linux/macOS
    source .venv/bin/activate
fi

echo "✅ Entorno virtual activado."

# --- 4. Instala dependencias ---
if [ -f "pyproject.toml" ]; then
    echo "📦 Instalando dependencias desde pyproject.toml con uv pip..."
    uv pip install -r pyproject.toml
else
    echo "⚠️  No se encontró pyproject.toml. Saltando instalación de dependencias."
fi

# --- 5. Corre los servidores ---
echo "🚀 Iniciando server.py y client.py en segundo plano..."

trap 'kill $(jobs -p)' EXIT
python server.py &
python client.py

