Antes de abrir aplicación, usar los siguientes comandos en git bash: <br />

py -m venv .venv <br />
source .venv/Scripts/activate <br />
pip install -r requirements.txt <br />
python manage.py makemigrations <br />
python manage.py migrate <br />
python manage.py createsuperuser <br />
python manage.py runserver <br />