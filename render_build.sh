#!/usr/bin/env bash
set -euo pipefail
rm -rf backend s2s_backend_deploy.zip s2s_backend_deploy.b64
cat backend_chunks/part*.txt > s2s_backend_deploy.b64
base64 -d s2s_backend_deploy.b64 > s2s_backend_deploy.zip
echo "cce8c941c703a2a4c512f88ebadb73763445970e2ef5100a1a0052a105ac026f  s2s_backend_deploy.zip" | sha256sum -c -
mkdir -p backend
unzip -q s2s_backend_deploy.zip -d backend
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py seed_s2s
python manage.py verify_s2s
