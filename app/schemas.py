# app/schemas.py

from pydantic import BaseModel
from typing import Optional, Dict

class TextoEntrada(BaseModel):
    texto: str

class ResultadoClasificacion(BaseModel):
    categoria: str
    confianza: float
    probabilidades: Dict[str, float]
    detalle: Optional[str] = None