from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import puntos_logisticos, rutas, simulaciones, transportes

app = FastAPI(
    title="Simulador Logístico Multimodal",
    description="API académica para comparar rutas, transportes, costos, tiempos y seguridad.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "API del simulador logístico activa"}


app.include_router(rutas.router, prefix="/api")
app.include_router(puntos_logisticos.router, prefix="/api")
app.include_router(transportes.router, prefix="/api")
app.include_router(simulaciones.router, prefix="/api")
