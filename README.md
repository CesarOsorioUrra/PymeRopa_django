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

La aplicación ahora si permite registrar ventas, compras, actulizar el inventario al vender y compras, eliminar todas las ventas o compras. Se puede publicar avisos. Se puede eliminar detalles de compra/venta mientras esta está en curso. Hay una página de adminstración donde se pueden crear, modificar, y eliminar usuarios, eliminar compras y ventas, modificar prendas, y modificar informaciones de los usuarios como sus salarios, y los avisos que estos vean en su página de inicio.<br />