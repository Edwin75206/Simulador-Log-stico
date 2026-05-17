# Scripts de base de datos

Hay dos formas de crear las tablas del proyecto.

## Opcion recomendada: Alembic

Desde la carpeta `backend`:

```bash
cd backend
alembic upgrade head
```

Alembic usa las migraciones del proyecto y crea las tablas necesarias en la base configurada en `.env`.

## Opcion manual: MySQL Workbench

Abre MySQL Workbench y ejecuta estos scripts en orden:

1. `backend/database/create_database.sql`
2. `backend/database/schema.sql`

Si usas Alembic, no es necesario ejecutar `schema.sql` manualmente.
