#!/usr/bin/env bash
set -euo pipefail
rm -rf backend
mkdir -p backend
unzip -q s2s_backend_deploy.zip -d backend
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py seed_s2s
python manage.py verify_s2s
