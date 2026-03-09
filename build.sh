#!/bin/bash
set -e

# Installer Node.js via nvm si pas disponible
if ! command -v node &> /dev/null; then
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    nvm install 20
    nvm use 20
fi

# Builder le frontend Vue
cd frontend
npm ci
npm run build
cd ..

# Installer les dépendances Python
pip install -r backend/requirements.txt
