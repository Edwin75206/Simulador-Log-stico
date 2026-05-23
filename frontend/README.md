# Frontend

Interfaz en React con Vite, Axios, React Router y Recharts.

## Configuracion

```bash
cd frontend
npm install
npm run dev
```

El frontend usa por defecto `http://localhost:8000/api`. Puedes cambiarlo creando un archivo `.env` con:

```bash
VITE_API_URL=http://localhost:8000/api
```

## Google Maps Embed

La pantalla de resultados puede mostrar un mapa embebido de Google Maps usando Google Maps Embed API.

1. Crea una API key en Google Cloud.
2. Habilita `Maps Embed API`.
3. Crea `frontend/.env` a partir de `frontend/.env.example`.
4. Agrega tu llave:

```bash
VITE_GOOGLE_MAPS_EMBED_API_KEY=tu_api_key
```

5. Reinicia el servidor:

```bash
npm run dev
```

El proyecto mantiene enlaces externos a Google Maps aunque no haya API key. El mapa embebido solo se muestra si se configura `VITE_GOOGLE_MAPS_EMBED_API_KEY`.
