# app/api.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.schemas import TextoEntrada, ResultadoClasificacion
from app.model_service import service

app = FastAPI(title="JustIA MVP", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Endpoint API
@app.post("/clasificar", response_model=ResultadoClasificacion)
def clasificar_texto(data: TextoEntrada):
    return service.clasificar(data.texto)

# 🔹 Servir carpeta public completa (debe ir después de las rutas API)
app.mount("/", StaticFiles(directory="public", html=True), name="public")

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app.api:app", host="0.0.0.0", port=port)