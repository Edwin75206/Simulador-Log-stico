# Backend

API REST con FastAPI, SQLAlchemy, Alembic y MySQL.

## Configuracion

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edita `.env` con tus credenciales de MySQL. La base `simulador_logistico` debe existir previamente.

## Migraciones y datos

```bash
alembic upgrade head
python app/seed/seed_data.py
```

## Ejecutar

```bash
uvicorn app.main:app --reload
```

API: `http://localhost:8000`
Docs: `http://localhost:8000/docs`
