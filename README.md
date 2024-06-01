# Ontake-api

## Run 
``` bash
# Install env
python3 -m venv env
# Run env
source env/bin/activate
# Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
# Make migrations and migrate
python manage.py makemigrations app_fte_justification
python manage.py migrate app_fte_justification
# Run Server
python manage.py runserver
```