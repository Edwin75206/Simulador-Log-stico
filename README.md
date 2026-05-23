# Simulador Logistico Multimodal

Aplicacion academica full stack para registrar puntos logisticos, rutas, transportes y ejecutar simulaciones logisticas multimodales con datos locales de prueba. El sistema calcula costos, tiempos estimados, riesgo, consumo y recomienda la mejor combinacion segun la prioridad elegida.

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

No se usa MongoDB ni APIs externas de pago. La integracion con Google Maps se hace con enlaces publicos, sin API Key.

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
cd ../frontend
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

- `puntos_logisticos`
- `rutas`
- `transportes`
- `simulaciones`
- `resultados_simulacion`

## Cargar datos de prueba

```bash
python app/seed/seed_data.py
```

El seed agrega puntos logisticos, rutas y transportes si no existen. No elimina registros previos.

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
8. Revisa puntos logisticos, rutas y transportes.
9. Crea una nueva simulacion, por ejemplo:
   - Origen: `Central de Abasto CDMX`
   - Destino: `Puerto de Veracruz`
   - Peso kg: `1000`
   - Tipo de mercancia: `Mercancia general`
   - Prioridad: `equilibrada`
10. Consulta la tabla y graficas de resultados.
11. Usa el boton `Ver ruta en Google Maps` para abrir la ruta en una pestaña nueva.

## Puntos logisticos

El sistema incluye un catalogo de puntos logisticos principales de Mexico:

- 6 centrales de abasto
- 6 puertos
- 6 centrales de autobuses
- 6 aeropuertos

Cada punto logistico tiene nombre, tipo, ciudad, estado, direccion o referencia, coordenadas opcionales y estado activo. Los tipos permitidos son:

- `central_abasto`
- `puerto`
- `central_autobuses`
- `aeropuerto`

La pantalla `Puntos logisticos` permite consultar los puntos, filtrar por tipo y abrir cada ubicacion en Google Maps.

## Google Maps sin API Key

El proyecto no usa Google Maps API ni requiere llave. Solo genera enlaces publicos:

```text
https://www.google.com/maps/search/?api=1&query=NOMBRE+CIUDAD+ESTADO
https://www.google.com/maps/dir/?api=1&origin=ORIGEN&destination=DESTINO&travelmode=driving
```

Si una ruta tiene puntos logisticos con coordenadas, el enlace puede usar `latitud,longitud`. Si no tiene coordenadas, usa nombre, ciudad y estado del punto logistico.

## Prueba multimodal recomendada

Despues de ejecutar migraciones y seed:

1. Entra a `Nueva simulacion`.
2. Selecciona:
   - Origen: `Central de Abasto CDMX`
   - Destino: `Puerto de Veracruz`
   - Peso kg: `1000`
   - Prioridad: `equilibrada`
3. Ejecuta la simulacion.
4. Revisa la ruta recomendada, tabla comparativa y graficas.
5. Abre el boton `Ver ruta en Google Maps`.

## Rutas generadas automaticamente

Al cargar el seed, el sistema recorre todos los puntos logisticos activos y crea una ruta por cada par de puntos que todavia no tenga ruta registrada. El backend mantiene la busqueda bidireccional, por lo que una sola ruta `A - B` tambien permite simular `B - A`.

Las rutas automaticas usan coordenadas aproximadas de los 24 puntos logisticos iniciales. La distancia se estima con Haversine y se multiplica por un factor de carretera academico; si un punto no tiene coordenadas, el seed usa una distancia simulada segun estado y tipo de punto.

Las casetas de esas rutas son aproximaciones academicas. La ruta guarda una caseta base por distancia y cada transporte terrestre aplica su factor:

```text
casetas_base = distancia_km * tarifa_simulada_por_km
casetas_ajustadas = casetas_base * factor_caseta
```

Regla simulada de caseta base:

- Menos de `80 km`: `$80`
- De `80 km` a `200 km`: `distancia_km * 2.2`
- De `201 km` a `500 km`: `distancia_km * 2.8`
- Mayor a `500 km`: `distancia_km * 3.2`

El seed redondea la caseta base al multiplo de 10 mas cercano. Por ejemplo, una ruta con caseta base `$370` y un `Full trailer refrigerado` con factor `2.1` produce casetas ajustadas de `$777`.

En el simulador los aviones, barcos y trenes no pagan casetas; esos resultados se muestran como `No aplica`.

## Casetas y peajes

El sistema guarda una caseta base estimada por ruta y la usa para calcular los peajes ajustados de las alternativas terrestres:

```text
casetas_ajustadas = casetas_base * factor_caseta
```

Si una ruta antigua no tiene caseta base, una simulacion nueva aplica la misma formula academica por distancia como fallback. Ejecutar `python app/seed/seed_data.py` tambien repara rutas de puntos logisticos con casetas vacias o en cero sin duplicarlas.

Los factores permiten comparar una camioneta con un trailer o full trailer. Para transporte `aereo`, `maritimo` y `ferroviario`, la interfaz muestra casetas como `No aplica`.

Las casetas son estimaciones para fines academicos. El proyecto no consulta peajes reales automaticamente para evitar costo, dependencia externa o errores por cambios de API. Una integracion futura podria evaluar:

- Google Routes API con `TollInfo` y precios estimados de peaje.
- SICT/Mappir `Traza tu Ruta`, si se dispone de una interfaz publica estable sin depender de scraping fragil.
- API de Ruteo de INEGI, considerando que sus tarifas pueden diferir de costos reales durante actualizaciones.

## Logica de calculo

Al crear una simulacion, el backend:

1. Busca rutas activas entre el origen y destino, aceptando ambos sentidos de la ruta registrada.
2. Busca transportes activos con capacidad suficiente para el peso.
3. Genera todas las combinaciones ruta-transporte.
4. Calcula costo, tiempo, riesgo, consumo y puntaje total.
5. Guarda la simulacion y sus resultados.
6. Marca como recomendada la mejor opcion.

Formula de costo con combustible:

```text
consumo_por_km = 1 / rendimiento_km_litro
consumo_total = distancia_km * consumo_por_km
costo_combustible = consumo_total * costo_combustible_litro
casetas_ajustadas = casetas_base * factor_caseta  # solo transporte terrestre
costo_total = costo_combustible + casetas_ajustadas + mantenimiento + costo_operativo
```

Si un transporte terrestre no tiene factor de caseta, el backend usa factor `1`. Para categoria `aereo`, `maritimo` o `ferroviario`, las casetas ajustadas son `0` y la interfaz muestra `No aplica`.

Si un transporte no tiene rendimiento o costo de combustible, el sistema usa la formula anterior como respaldo y conserva las reglas de casetas por categoria:

```text
costo_total = (distancia_km * costo_km) + casetas_ajustadas + mantenimiento + costo_operativo
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

Compatibilidad por mercancia:

```text
perecedera -> permite transportes perecedera o mixta
no_perecedera -> permite transportes no_perecedera o mixta
mixta -> permite todos
```

Los valores de rendimiento, combustible, casetas y costos son academicos simulados para comparacion. No representan tarifas oficiales ni cotizaciones reales.

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
