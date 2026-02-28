# ============================================
# MVP - Clasificador Jurídico con Métricas Avanzadas
# ============================================

import os
import json
import time
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
nltk.download("stopwords") 

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# ==========================================================
# CONFIGURACIÓN DE RUTAS
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "dataset_juridico_300_definitivo.json")
MODEL_DIR = os.path.join(BASE_DIR, "model")

os.makedirs(MODEL_DIR, exist_ok=True)

# ==========================================================
# 1️⃣ CARGAR DATASET
# ==========================================================

with open(DATA_PATH, encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

print(f"✅ Dataset cargado correctamente. Total registros: {len(df)}")
print(DATA_PATH)
print("\nDistribución por categoría:")
print(df["categoria"].value_counts())

# ==========================================================
# 2️⃣ DIVISIÓN TRAIN / TEST
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    df["texto"],
    df["categoria"],
    test_size=0.2,
    random_state=42,
    stratify=df["categoria"]
)

# ==========================================================
# 3️⃣ PIPELINE
# ==========================================================
from nltk.corpus import stopwords
spanish_stopwords = stopwords.words("spanish")

modelo = Pipeline([
    ("tfidf", TfidfVectorizer(
    ngram_range=(1,1),
    stop_words=spanish_stopwords
)),
    ("clf",LogisticRegression(
    max_iter=2000,
    multi_class="multinomial",
    solver="lbfgs"
) )
])

# ==========================================================
# 4️⃣ ENTRENAMIENTO
# ==========================================================

print("\n🔄 Entrenando modelo...")
start_time = time.time()

modelo.fit(X_train, y_train)

train_time = round(time.time() - start_time, 4)
print(f"✅ Entrenamiento completado en {train_time} segundos.")

# ==========================================================
# 5️⃣ EVALUACIÓN EN TEST
# ==========================================================

print("\n📊 Evaluando modelo...")
start_time = time.time()

y_pred = modelo.predict(X_test)

predict_time = round(time.time() - start_time, 4)
print(f"⏱ Tiempo de predicción: {predict_time} segundos.")

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average="weighted")
recall = recall_score(y_test, y_pred, average="weighted")
f1 = f1_score(y_test, y_pred, average="weighted")

print("\n=== MÉTRICAS ===")
print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-Score:  {f1:.4f}")

print("\nReporte detallado:")
print(classification_report(y_test, y_pred))

# ==========================================================
# 6️⃣ VALIDACIÓN CRUZADA
# ==========================================================

print("\n🔎 Ejecutando validación cruzada (5-fold)...")

cv_scores = cross_val_score(modelo, df["texto"], df["categoria"], cv=5)

print("Scores por fold:", cv_scores)
print("Accuracy promedio CV:", np.mean(cv_scores))

# ==========================================================
# 7️⃣ MATRIZ DE CONFUSIÓN
# ==========================================================

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d",
            xticklabels=modelo.classes_,
            yticklabels=modelo.classes_,
            cmap="Blues")

plt.title("Matriz de Confusión")
plt.xlabel("Predicción")
plt.ylabel("Real")
plt.tight_layout()

conf_matrix_path = os.path.join(MODEL_DIR, "matriz_confusion.png")
plt.savefig(conf_matrix_path)
plt.show()

print(f"\n📌 Matriz de confusión guardada en: {conf_matrix_path}")

# ==========================================================
# 8️⃣ GUARDAR MODELO
# ==========================================================

model_path = os.path.join(MODEL_DIR, "modelo_clasificador_justia.pkl")
joblib.dump(modelo, model_path)

print(f"\n💾 Modelo guardado en: {model_path}")
print("\n🎉 Proceso finalizado correctamente.")