# 🧪 Casos de Prueba — JustIA MVP

Textos para validar el comportamiento del clasificador. Copiar y pegar cada caso en el frontend o en la API directamente.

---

## ✅ Casos claros — alta confianza esperada

### 1. Laboral
```
El trabajador interpuso demanda por terminación unilateral del contrato y solicitó el pago de prestaciones sociales adeudadas conforme al marco normativo vigente.
```

### 2. Penal
```
La fiscalía presentó acusación formal por conducta punible relacionada con fraude procesal y solicitó medida restrictiva de libertad.
```

### 3. Civil
```
La parte actora presentó demanda por incumplimiento de obligación contractual y reclamó indemnización por daños patrimoniales derivados del contrato de compraventa.
```

### 4. Familia
```
La madre del menor solicitó revisión de cuota alimentaria y regulación del régimen de visitas en atención al interés superior del menor.
```

### 5. Constitucional
```
El accionante interpuso acción de tutela por vulneración del derecho fundamental al debido proceso y solicitó protección inmediata.
```

---

## 🟡 Casos ambiguos — pueden activar revisión humana

### 6. Laboral + Constitucional
```
El trabajador interpuso acción judicial alegando vulneración del derecho al mínimo vital tras la terminación de su contrato de trabajo.
```

### 7. Civil + Penal
```
Se analiza la posible responsabilidad jurídica derivada de un incumplimiento contractual que podría constituir conducta punible.
```

### 8. Familia + Constitucional
```
Durante el proceso de custodia se alegó vulneración de derechos fundamentales del menor y se solicitó intervención judicial urgente.
```

### 9. Caso altamente ambiguo
```
En el marco de un conflicto jurídico, las partes presentaron recurso judicial alegando afectación grave y vulneración de garantías procesales.
```

### 10. Caso general — probable revisión humana
```
Se presentó demanda ante el juez competente solicitando revisión del proceso en curso y valoración probatoria conforme al marco normativo aplicable.
```

---

## 📋 Referencia rápida

| # | Tipo esperado | Confianza esperada |
|---|---------------|--------------------|
| 1 | Laboral | Alta |
| 2 | Penal | Alta |
| 3 | Civil | Alta |
| 4 | Familia | Alta |
| 5 | Constitucional | Alta |
| 6 | Laboral / Constitucional | Media — posible revisión |
| 7 | Civil / Penal | Media — posible revisión |
| 8 | Familia / Constitucional | Media — posible revisión |
| 9 | Ambiguo | Baja — revisión humana |
| 10 | Ambiguo general | Baja — revisión humana |
