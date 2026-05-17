# Simulador Logistico Multimodal

Aplicacion academica full stack para registrar rutas, registrar transportes y ejecutar simulaciones logisticas multimodales con datos locales de prueba. El sistema calcula costos, tiempos estimados, riesgo, consumo y recomienda la mejor combinacion segun la prioridad elegida.

## Tecnologias

- Frontend: React, Vite, Axios, React Router, Recharts, CSS
- Backend: Python, FastAPI, SQLAlchemy, Alembic, Pydantic
- Base de datos: MySQL
- Driver MySQL: PyMySQL

## Requisitos previos

- Python 3.11 o superior
- Node.js 20 o superior
- MySQL corriendo localmente
- Base de datos vacia ya creada: `simulador_logistico`

No se usa MongoDB, Google Maps, APIs externas ni integraciones de mapas reales.

## Instalacion en una nueva computadora

1. Instala Git.
2. Instala Python 3.11 o superior.
3. Instala Node.js 20 o superior.
4. Instala MySQL Server y MySQL Workbench.
5. Clona el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
cd simulador-logistico
```

6. Crea la base de datos desde MySQL Workbench ejecutando:

```text
backend/database/create_database.sql
```

7. Configura el backend:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

8. Edita `backend/.env` con tus credenciales locales:

```bash
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=simulador_logistico
```

Si MySQL esta configurado en otro puerto, por ejemplo `3307`, cambia `DB_PORT` en el archivo `.env`.

9. Ejecuta migraciones con Alembic:

```bash
alembic upgrade head
```

10. Carga datos de prueba:

```bash
python app/seed/seed_data.py
```

11. Levanta el backend:

```bash
uvicorn app.main:app --reload
```

12. En otra terminal, levanta el frontend:

```bash
cd frontend
npm install
npm run dev
```

La API quedara en `http://localhost:8000` y el frontend en `http://localhost:5173`.

## Configurar backend

```bash
cd simulador-logistico/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edita `.env` con tus credenciales reales:

```bash
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=simulador_logistico
```

La base de datos debe existir antes de correr migraciones. Este proyecto no hace `DROP DATABASE` ni borra la base completa.

## Ejecutar migraciones

```bash
alembic upgrade head
```

Esto crea las tablas:

- `rutas`
- `transportes`
- `simulaciones`
- `resultados_simulacion`

## Cargar datos de prueba

```bash
python app/seed/seed_data.py
```

El seed agrega rutas y transportes si no existen. No elimina registros previos.

## Iniciar backend

```bash
uvicorn app.main:app --reload
```

URLs utiles:

- API: `http://localhost:8000`
- Health check: `http://localhost:8000/api/health`
- Swagger: `http://localhost:8000/docs`

## Configurar frontend

Abre otra terminal:

```bash
cd simulador-logistico/frontend
npm install
npm run dev
```

La app queda disponible en:

```bash
http://localhost:5173
```

Por defecto el frontend apunta a `http://localhost:8000/api`. Si necesitas cambiarlo, crea `frontend/.env`:

```bash
VITE_API_URL=http://localhost:8000/api
```

## Flujo de uso

1. Inicia MySQL y confirma que existe la base `simulador_logistico`.
2. Configura `backend/.env`.
3. Ejecuta `alembic upgrade head`.
4. Ejecuta `python app/seed/seed_data.py`.
5. Inicia el backend con `uvicorn app.main:app --reload`.
6. Inicia el frontend con `npm run dev`.
7. Entra a `http://localhost:5173`.
8. Revisa rutas y transportes.
9. Crea una nueva simulacion, por ejemplo:
   - Origen: `Puebla`
   - Destino: `CDMX`
   - Peso kg: `1000`
   - Tipo de mercancia: `Mercancia general`
   - Prioridad: `equilibrada`
10. Consulta la tabla y graficas de resultados.

## Logica de calculo

Al crear una simulacion, el backend:

1. Busca rutas activas entre el origen y destino, aceptando ambos sentidos de la ruta registrada.
2. Busca transportes activos con capacidad suficiente para el peso.
3. Genera todas las combinaciones ruta-transporte.
4. Calcula costo, tiempo, riesgo, consumo y puntaje total.
5. Guarda la simulacion y sus resultados.
6. Marca como recomendada la mejor opcion.

Formula de costo:

```text
costo_total = (distancia_km * costo_km) + casetas + mantenimiento + costo_operativo
```

Formula de tiempo:

```text
tiempo_base = distancia_km / velocidad_promedio
tiempo_estimado_horas = tiempo_base * factor_trafico
```

Factores de trafico:

```text
1 = 1.05
2 = 1.15
3 = 1.30
4 = 1.45
5 = 1.60
```

Riesgo:

```text
riesgo_ruta = promedio(riesgo, trafico, estado_carretera, inseguridad)
riesgo_transporte = 6 - seguridad
puntaje_riesgo = promedio(riesgo_ruta, riesgo_transporte)
```

Consumo:

```text
consumo_total = distancia_km * consumo_por_km
```

Puntaje equilibrado:

```text
puntaje_total =
  costo_normalizado * 0.35 +
  tiempo_normalizado * 0.30 +
  riesgo_normalizado * 0.25 +
  consumo_normalizado * 0.10
```

Criterios de recomendacion:

- `costo`: menor costo total
- `tiempo`: menor tiempo estimado
- `seguridad`: menor puntaje de riesgo
- `recursos`: menor consumo total
- `equilibrada`: menor puntaje total normalizado

## Si falla la conexion con MySQL

- Verifica que MySQL este encendido.
- Confirma que la base `simulador_logistico` exista en MySQL Workbench.
- Revisa usuario, password, host y puerto en `backend/.env`.
- Si usas password con caracteres especiales, codificalos para URL o usa una clave simple durante pruebas locales.
- Comprueba que puedes entrar con el mismo usuario desde MySQL Workbench.
- Reintenta `alembic upgrade head` desde la carpeta `backend`.
