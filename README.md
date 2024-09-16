# Event App Backend

Este repositorio contiene el backend de una web para gestionar eventos y usuarios. Desarrollada con FastAPI, SQLAlchemy, pydantic y JWT. Puedes visitar el repositorio del frontend [aqui](https://github.com/SonicWD/Web-FronEnd-My-event-management-platform).

## Clonar Repositorio

Para clonar este repositorio, utiliza el siguiente comando:

```bash
git clone https://github.com/LASM24/event_app_backend.git
```

## Configuración del Entorno Virtual

Se recomienda usar un entorno virtual para instalar las dependencias del proyecto. A continuación, se muestra cómo configurarlo:

1. **Crear un entorno virtual:**

   ```bash
   python -m venv event-fapi
   ```

3. **Activar el entorno virtual:**

   - En Windows:

     ```bash
     .\event-fapi\Scripts\activate
     ```

   - En macOS/Linux:

     ```bash
     source event-fapi/bin/activate
     ```

## Instalación de Dependencias

Para instalar las dependencias necesarias, ejecuta el siguiente comando dentro del directorio clonado:

```bash
pip install -r requirements.txt
```

## Ejecutar el Servidor

Para ejecutar el servidor de desarrollo de FastAPI, asegúrate de que tu entorno virtual esté activo y luego ejecuta el siguiente comando:

```bash
uvicorn app.main:app --reload
```

Esto iniciará el servidor en `http://localhost:8000`. Puedes acceder a la documentación de la API en `http://localhost:8000/docs`. Tener en cuenta que la rama main esta configurada para el entorno de produccion, así que se debe inicar en la rama main usando el comando:

```
git checkout develop
```

## Descripción de la API

La API proporciona los siguientes endpoints:

- **Registrarse:** `POST /user-register`
  - Crea un nuevo usuario con nombre de usuario, correo electrónico y contraseña.

- **Iniciar Sesión:** `POST /login`
  - Permite a los usuarios existentes iniciar sesión mediante nombre de usuario y contraseña.

- **Crear Evento:** `POST /events-create`
  - Crea un nuevo evento con título, descripción, fecha.

- **Listar Eventos:** `GET /events`
  - Obtiene una lista de todos los eventos registrados.

- **Registrarse en un Evento:** `POST /events/{event_id}/register`
  - Registra un usuario para participar en un evento específico.

- **Ver Registrados en un Evento:** `GET /events/{event_id}/registrations`
  - Obtiene una lista de usuarios registrados para un evento específico.

