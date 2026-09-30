#!/usr/bin/env bash
# ស្គ្រីបនេះនឹងត្រូវបានប្រតិបត្តិដោយ Render មុននឹង deploy
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
