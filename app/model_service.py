# app/model_service.py

import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "modelo_clasificador_justia.pkl")

UMBRAL_CONFIANZA = 0.40
MAX_CARACTERES = 2000

class ClasificadorService:
    def __init__(self):
        self.modelo = joblib.load(MODEL_PATH)

    def clasificar(self, texto: str):


        if len(texto) > MAX_CARACTERES:
            return {
                "categoria": "texto_demasiado_extenso",
                "confianza": 0.0,
                "detalle": f"El texto supera el límite permitido de {MAX_CARACTERES} caracteres."
            }

        pred = self.modelo.predict([texto])[0]
        probs = self.modelo.predict_proba([texto])[0]

        max_confianza = float(max(probs))

        resultado = {
            "categoria": pred,
            "confianza": max_confianza,
            "probabilidades": {
                clase: float(prob)
                for clase, prob in zip(self.modelo.classes_, probs)
            }
        }

        # Aplicar umbral
        if max_confianza < UMBRAL_CONFIANZA:
            resultado["categoria"] = "requiere_revision_humana"
            resultado["detalle"] = "Nivel de confianza insuficiente para clasificación automática."

        return resultado


service = ClasificadorService()