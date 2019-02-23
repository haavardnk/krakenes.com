#!/bin/bash
. .bashrc
DEPLOY_DIR=~/krakenescom
cd "$DEPLOY_DIR"
echo "# Starting deployment."
set -e # Fail the script on any errors.
git pull
echo "# Navigating to the root directory."
cd ..
echo "# Activating virtualenv."
set +e # The activate script might return non-zero even on success. 
source myenv/bin/activate
set -e
echo "# Navigating to the DEPLOY directory."
cd "$DEPLOY_DIR"
echo "# Installing pip requirements."
pip install -r requirements.txt
echo "# Collecting static files."
python manage.py collectstatic --noinput
echo "# Making database migrations."
python manage.py makemigrations --noinput
echo "# Running database migrations."
python manage.py migrate --noinput
echo "# Restarting the backend service."
sudo systemctl restart gunicorn
set +e
echo "# Deployment done!"