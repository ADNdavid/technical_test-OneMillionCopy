# OneMillionCopy — API de Leads

 **Resumen del proyecto:**
 - Objetivo: API REST para registrar y consultar leads que provienen de distintos embudos y generar un resumen ejecutivo usando IA.

 **Tecnologías principales:**
 - `FastAPI`: framework rápido y simple para APIs, buena para prototipos y producción.
 - `SQLModel` + `pymysql`: modelado y acceso a MySQL con tipado y conveniencia (SQLModel sobre SQLAlchemy).
 - `httpx`: cliente HTTP asíncrono para llamadas a APIs externas (p. ej. OpenAI).
 - `Faker`: generar datos de prueba para el seed.
 - `Docker` + `docker-compose`: aislar la app y la base de datos para desarrollo y pruebas reproducibles.


 Requisitos
 - Python >= 3.13
 - Docker (opcional para levantar contenedores)
 - XAMPP (opcional si no se cuenta con Docker)

## Instalación y Uso

Clonar el repositorio:
```bash
git clone https://github.com/ADNdavid/technical_test-OneMillionCopy
cd technical_test-OneMillionCopy
```

 Instalación (local, sin Docker)
 1. Crear y activar un entorno virtual:

 ```bash
 python -m venv .venv
 source .venv/Scripts/activate
 ```

 2. Instalar dependencias desde `pyproject.toml`:

 ```bash
 python -m pip install --upgrade uv
 python uv sync
 ```

 3. Configurar variables de entorno:

 ```bash
 cp .env.example .env
 # Editar .env con tus valores reales (especialmente OPENAI_API_KEY)
 ```

 Ejecución
 - Con Docker (recomendado para reproducibilidad):

 ```bash
 docker compose up --build
 ```

 - Sin Docker (Encender Servidor Apache + mySQL en XAMPP):

 ```bash
 uvicorn main:app --reload --port 8000
 ```

 Variables de entorno importantes
 - `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB_NAME` — conexión a MySQL.
 - `OPENAI_API_KEY` — clave para el servicio de IA.
 - `OPENAI_MODEL` — modelo a usar para generar el resumen.

 Creación de esquemas / tablas
 - La aplicación crea las tablas en el arranque usando la configuración de `db.create_all_tables` (se ejecuta en el lifespan de FastAPI).

 Seed (datos de prueba)
 - La forma más simple de poblar datos fake (seed) es llamar al endpoint que genera leads falsos `generate_fake_leads`.

 Endpoints principales
 - Crear lead: `POST /api/leads`
 - Listar leads: `GET /api/leads`
 - Obtener lead por id: `GET /api/leads/{lead_id}`
 - Actualizar: `PATCH /api/leads/{lead_id}`
 - Borrar (hard delete): `DELETE /api/leads/{lead_id}`
 - Borrar (soft delete): `DELETE /api/leads/{lead_id}/soft`
 - Estadísticas: `GET /api/leads/stats/`
 - Resumen por IA: `GET /api/leads/ai/summary`



 Notas sobre IA
 - El endpoint de resumen `GET /api/leads/ai/summary` recopila leads (según filtros) y llama a la API de OpenAI usando `httpx`. Debes exportar `OPENAI_API_KEY` y `OPENAI_MODEL` para que funcione.

 Archivo principal
 - `main.py`: inicializa la app y registra el router de leads.

 Estructura relevante
 - `app/models/leads.py`: definición del modelo `Lead`.
 - `app/routers/leads.py`: rutas HTTP.
 - `app/services/leads.py`: lógica de negocio, generación de fake leads y llamada a IA.
 - `db.py`: motor y dependencias de sesión.

 Soporte y pruebas rápidas
 - La app expone la documentación automática de OpenAPI en `http://localhost:8000/docs` cuando esté corriendo.

## Author

- GitHub - [@ADNdavid](https://github.com/ADNdavid)
- LinkedIn - [Anderson Sepúlveda](https://www.linkedin.com/in/adndavid/)