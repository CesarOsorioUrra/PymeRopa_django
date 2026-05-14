Antes de abrir aplicación, usar los siguientes comandos en git bash: <br />

py -m venv .venv <br />
source .venv/Scripts/activate <br />
pip install -r requirements.txt <br />
python manage.py makemigrations <br />
python manage.py migrate <br />
python manage.py createsuperuser <br />
python manage.py runserver <br />

El super usuario puede acceder a la página para registrar compras, ver el inventario, enviar avisos a otros usuarios, y también puede acceder a la página de administración de django para crear nuevos usuarios.<br />
Si se crea un usuario que no sea parte del "staff", entonces ese usuario será un empleado, el cual puede acceder a la página para registrar ventas y ver el inventario. No puede acceder a la página para registrar compras, no puede acceder a la página de dministración, y tampoco puede publicar avisos.<br />

La aplicación aún no permite registrar compras, registrar ventas, publicar avisos, y tampoco se puede actualizar el inventario. <br />