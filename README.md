# ms-adoptapp-python

Backend de Django para gestion de adopciones de mascotas.

## Requisitos

- Python 3.12 o superior.
- PostgreSQL en ejecucion.
- Un entorno virtual activo.

## Variables de entorno

El proyecto lee un archivo `.env` en la raiz del proyecto. Crea uno con este formato:

```env
DEBUG=True
SECRET_KEY=tu_clave_secreta
DATABASE_URL=postgres://usuario:password@localhost:5432/adoptapp_db
```

## Pasos para iniciar el proyecto

1. Clona el repositorio y entra a la carpeta del proyecto.
2. Crea el entorno virtual si no existe:

```powershell
python -m venv venv
```

3. Activa el entorno virtual en PowerShell:

```powershell
.\venv\Scripts\Activate
```

Si usas bash, activa el entorno con:

```bash
source venv/Scripts/activate
```

4. Instala las dependencias:

```powershell
pip install -r requirements.txt
```

5. Configura el archivo `.env` con la conexion a PostgreSQL.

6. Crea las migraciones iniciales del app `core` y luego ejecuta las migraciones:

```powershell
python manage.py makemigrations core
python manage.py migrate
```

7. Crea un usuario administrador si lo necesitas:

```powershell
python manage.py createsuperuser
```

8. Levanta el servidor de desarrollo:

```powershell
python manage.py runserver
```

9. Abre el proyecto en:

- `http://127.0.0.1:8000/admin/` para el panel de administracion.
- `http://127.0.0.1:8000/api/` para los endpoints de la API.

## Problemas comunes

- Si aparece un error relacionado con `environ`, instala `django-environ` en el entorno virtual.
- Si la base de datos no conecta, revisa que PostgreSQL este activo y que `DATABASE_URL` tenga los datos correctos.
