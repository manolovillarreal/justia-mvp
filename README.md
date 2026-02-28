# 📘 JustIA MVP
### Sistema de Clasificación Automática de Textos Jurídicos

---

## 📌 Descripción

**JustIA MVP** es un sistema de clasificación automática de textos jurídicos desarrollado como producto mínimo viable (MVP).

Permite categorizar fragmentos de texto en cinco áreas del derecho:

- Laboral
- Penal
- Civil
- Familia
- Constitucional

El sistema utiliza:

- Representación **TF-IDF**
- **Logistic Regression** multiclase
- Umbral de confianza para **revisión humana**
- API REST con **FastAPI**
- Frontend estático servido desde la misma aplicación

> ⚠️ El modelo actúa como herramienta de apoyo y **no reemplaza el criterio profesional**.

---

## 🏗️ Arquitectura del Proyecto

```
justia-mvp/
│
├── app/
│   ├── api.py
│   ├── model_service.py
│   └── schemas.py
│
├── public/
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
├── model/
│   └── modelo_clasificador_justia.pkl
│
├── data/
│   └── dataset_juridico_300_definitivo.json
│
├── train_model.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Requisitos

- Python 3.9+
- pip
- Entorno virtual recomendado

---

## 🚀 Instalación

### 1️⃣ Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd justia-mvp
```

### 2️⃣ Crear entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

o:

```bash
pip install fastapi uvicorn scikit-learn pandas numpy joblib matplotlib seaborn
```

---

## 🧠 Entrenamiento del Modelo

El modelo se entrena con:

- TF-IDF (`ngram_range=(1,1)`)
- `LogisticRegression` (multinomial)

### 1️⃣ Ubicar el dataset

Colocar el archivo JSON dentro de:

```
data/dataset_juridico_300_definitivo.json
```

Formato esperado:

```json
[
  {
    "texto": "Texto jurídico...",
    "categoria": "laboral"
  }
]
```

### 2️⃣ Ejecutar entrenamiento

```bash
python train_model.py
```

Esto:
- Entrena el modelo
- Evalúa métricas
- Guarda el modelo en `model/modelo_clasificador_justia.pkl`

---

## 🌐 Ejecutar la API

Desde la raíz del proyecto:

```bash
uvicorn app.api:app --reload
```

La aplicación estará disponible en:

```
http://127.0.0.1:8000
```

---

## 🖥️ Frontend

El frontend es estático y se sirve desde `/public`.

Acceder en navegador:

```
http://127.0.0.1:8000
```

Permite:
- Ingresar texto jurídico (mínimo 50, máximo 2000 caracteres)
- Visualizar la categoría detectada
- Ver el nivel de confianza del modelo
- Ver la distribución de probabilidades por clase
- Detectar casos que requieren revisión humana

---

## 🔌 Consumo de la API

### Endpoint

```
POST /clasificar
```

### Body JSON

```json
{
  "texto": "El trabajador interpuso demanda por despido injustificado."
}
```

### Respuesta — clasificación automática

```json
{
  "categoria": "laboral",
  "confianza": 0.82,
  "probabilidades": {
    "laboral": 0.82,
    "civil": 0.05,
    "penal": 0.04,
    "familia": 0.03,
    "constitucional": 0.06
  }
}
```

### Respuesta — requiere revisión humana

```json
{
  "categoria": "requiere_revision_humana",
  "confianza": 0.28,
  "probabilidades": { "..." : "..." },
  "detalle": "Nivel de confianza insuficiente para clasificación automática."
}
```

---

## 🛡️ Umbral de Confianza

El sistema implementa un umbral mínimo de **0.40**.

Si la probabilidad máxima es menor a ese valor:

- → Se envía a **revisión humana**
- → No se clasifica automáticamente

Esto garantiza responsabilidad y control en entornos jurídicos.

---

## 📏 Límites del Sistema

| Límite | Detalle |
|--------|---------|
| Entrada máxima | 2000 caracteres |
| Entrada mínima | 50 caracteres |
| Archivos PDF | ❌ No soportado |
| OCR | ❌ No soportado |
| Documentos largos | ❌ No soportado |

---

## 🎯 Modelo Final Seleccionado

| Componente | Detalle |
|------------|---------|
| Representación | TF-IDF (unigramas) |
| Clasificador | LogisticRegression (multinomial) |
| Validación cruzada promedio | ~75% |
| Dataset | Con ambigüedad semántica realista |

Se seleccionó `LogisticRegression` por:

- Probabilidades calibradas
- Interpretabilidad
- Estabilidad
- Adecuación para API REST

---

## 🔮 Mejoras Futuras

- [ ] Integrar embeddings semánticos (SentenceTransformers)
- [ ] Implementar BERT en español
- [ ] Aceptar documentos PDF con pipeline de limpieza
- [ ] Incorporar explicabilidad avanzada (SHAP / LIME)
- [ ] Implementar autenticación por API key
- [ ] Despliegue en producción (Render / Docker)

---

## 📚 Consideraciones Éticas

Este sistema:

- **No reemplaza** el criterio jurídico humano
- Funciona como **apoyo preliminar** de clasificación
- Implementa un **umbral de revisión** para casos inciertos
- **No toma decisiones vinculantes**

---

## 👨‍💻 Autor

Proyecto desarrollado como ejercicio académico en el marco de:

> *Inteligencia Artificial aplicada al Desarrollo de Software.*

---

## 📄 Licencia

Uso académico.
