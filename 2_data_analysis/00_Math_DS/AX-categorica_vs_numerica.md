# Variables categóricas vs numéricas en Ciencia de Datos

En ciencia de datos, solemos distinguir entre **variables categóricas** y **variables numéricas** porque el tipo de dato determina qué análisis, modelos o visualizaciones se pueden aplicar.  

---

## 🔹 Variables categóricas
- **Definición:** Representan *categorías* o *etiquetas*. No tienen un orden matemático natural.  
- **Ejemplos:**
  - Género: `["Hombre", "Mujer", "Otro"]`
  - País: `["España", "México", "Argentina"]`
  - Estado civil: `["Soltero", "Casado", "Divorciado"]`
- **Tipos de categóricas:**
  - **Nominales:** No tienen orden lógico (ej. colores: rojo, azul, verde).
  - **Ordinales:** Tienen un orden implícito, aunque no una distancia exacta (ej. niveles educativos: primaria < secundaria < universidad).

👉 Se suelen codificar con técnicas como:
- **One-hot encoding** (variables ficticias/dummies).  
- **Label encoding** (convertir categorías a números, útil para ordinales).  

---

## 🔹 Variables numéricas
- **Definición:** Representan cantidades que sí admiten operaciones matemáticas.  
- **Ejemplos:**
  - Edad: `25, 40, 60`
  - Ingresos: `1500.50, 3200.75`
  - Altura: `1.75, 1.82`
- **Tipos de numéricas:**
  - **Discretas:** Valores enteros, contables (ej. número de hijos, cantidad de coches).
  - **Continuas:** Valores en un rango infinito, medibles (ej. peso, temperatura).  

👉 Con ellas puedes calcular:
- Media, varianza, desviación estándar.
- Correlaciones.
- Usarlas directamente en modelos de ML sin necesidad de codificación.  

---

## 📊 Diferencia clave

| Aspecto            | Categórica                   | Numérica                |
|--------------------|-----------------------------|-------------------------|
| Naturaleza         | Etiquetas o categorías      | Cantidades medibles     |
| Operaciones válidas| Conteo, frecuencia          | Media, suma, correlación|
| Ejemplo            | "Rojo", "Verde", "Azul"     | 1.65m, 75kg, 30 años    |

---

👉 En resumen:  
- **Categórica = qué clase es** (grupo, etiqueta).  
- **Numérica = cuánto mide** (cantidad, magnitud).  
