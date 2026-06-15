Antes de abrir aplicación, usar los siguientes comandos en git bash: <br />

py -m venv .venv <br />
source .venv/Scripts/activate <br />
pip install -r requirements.txt <br />
python manage.py makemigrations <br />
python manage.py migrate <br />
python manage.py createsuperuser <br />
python manage.py runserver <br />

El super usuario (administrador, puede haber más de uno) puede acceder a la página para registrar compras, ver el inventario, enviar avisos a otros usuarios, y también puede acceder a una página de administración en donde podrá crear nuevos usuarios, modificarlos, o eliminarlos (un administrador no podrá eliminarse a si mismo). También podrá modificar el nombre, descripción, y precio unitario de las prendas. Podrá eliminar compras y ventas. Podrá además modificar información adicional de los usuarios como sus salarios, o eliminar los avisos que se hayn publicado a estos.<br />

Si se crea un usuario que no sea parte del "staff", entonces ese usuario será un empleado, el cual puede acceder a la página para registrar ventas y ver el inventario. No puede acceder a la página para registrar compras, no puede acceder a la página de administración, y tampoco puede publicar avisos.<br />

La aplicación permite registrar ventas, compras, actualizar el inventario al vender y al comprar, eliminar todas las ventas o compras. Se puede publicar avisos. Se puede eliminar detalles de compra/venta mientras estas estén en curso. Hay una página de administración en donde se pueden crear, modificar, y eliminar usuarios, eliminar compras y ventas, modificar prendas, y modificar informaciones de los usuarios como sus salarios, y los avisos que estos vean en su página de inicio.<br />