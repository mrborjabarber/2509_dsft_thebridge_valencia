# streamlit_app.py
# ---------------------------------------------------------
# 💡 EJEMPLO BÁSICO DE STREAMLIT
# 
# Descripción: Pequeña app para mostrar cómo funciona Streamlit
# ---------------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------------
# 1️⃣ TÍTULO Y DESCRIPCIÓN
# ---------------------------------------------------------
st.title("🔢 Mini App: Calculadora de Cuadrado")
st.write("""
Esta pequeña aplicación demuestra cómo:
1. Recibir datos del usuario  
2. Procesarlos en Python  
3. Mostrar resultados y gráficos de forma interactiva 🎨
""")

# ---------------------------------------------------------
# 2️⃣ ENTRADA DEL USUARIO
# ---------------------------------------------------------
# Creamos una entrada numérica
numero = st.number_input("Introduce un número:", min_value=1, max_value=100, value=5)

# ---------------------------------------------------------
# 3️⃣ PROCESAMIENTO
# ---------------------------------------------------------
cuadrado = numero ** 2

# ---------------------------------------------------------
# 4️⃣ SALIDA DE TEXTO
# ---------------------------------------------------------
st.success(f"El cuadrado de {numero} es {cuadrado}")

# ---------------------------------------------------------
# 5️⃣ GRÁFICO INTERACTIVO
# ---------------------------------------------------------
# Creamos una tabla de valores del 1 al número introducido
valores = np.arange(1, numero + 1)
datos = pd.DataFrame({
    'Número': valores,
    'Cuadrado': valores ** 2
})

st.write("### 📊 Tabla de valores")
st.dataframe(datos)

# Mostramos un gráfico de línea
st.write("### 📈 Gráfico del cuadrado")
st.line_chart(datos.set_index('Número'))

# ---------------------------------------------------------
# 6️⃣ EXTRA: Slider para personalizar
# ---------------------------------------------------------
color_opcion = st.radio(
    "¿Qué color prefieres para la cabecera?",
    ("🌿 Verde", "💙 Azul", "❤️ Rojo")
)

# Cambiamos color del título según selección
if color_opcion == "🌿 Verde":
    st.markdown("<h2 style='color:green;'>¡Gracias por probar Streamlit!</h2>", unsafe_allow_html=True)
elif color_opcion == "💙 Azul":
    st.markdown("<h2 style='color:blue;'>¡Gracias por probar Streamlit!</h2>", unsafe_allow_html=True)
else:
    st.markdown("<h2 style='color:red;'>¡Gracias por probar Streamlit!</h2>", unsafe_allow_html=True)
