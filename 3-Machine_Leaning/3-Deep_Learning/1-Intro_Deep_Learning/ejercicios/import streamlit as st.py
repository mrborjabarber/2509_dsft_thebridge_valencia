import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Carga del modelo entrenado
# Asegúrate de haber guardado tu modelo:
# model_2.save("modelo_fashion.h5")
model = tf.keras.models.load_model("modelo_fashion.h5")

# Etiquetas de Fashion-MNIST
class_names = [
    "Camiseta/top",
    "Pantalón",
    "Jersey",
    "Vestido",
    "Abrigo",
    "Sandalia",
    "Camisa",
    "Zapatilla deportiva",
    "Bolso",
    "Botín"
]

# Interfaz Streamlit
st.title("Clasificador de Moda (Fashion-MNIST)")
st.write("Sube una imagen de ropa en blanco y negro (28×28) o deja que la app la convierta automáticamente.")

# Subir imagen
img_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])

if img_file is not None:
    # Mostrar imagen original
    image = Image.open(img_file).convert("L")  # Convertir a escala de grises
    st.image(image, caption="Imagen subida", use_column_width=True)

    # Preprocesamiento para el modelo
    img_resized = image.resize((28, 28))
    img_arr = np.array(img_resized) / 255.0  # Normalizar
    img_arr = img_arr.reshape(1, 28, 28)     # Añadir dimensión batch

    # Predicción
    prediction = model.predict(img_arr)
    class_id = np.argmax(prediction)
    confidence = np.max(prediction)

    # Mostrar resultado
    st.subheader("Predicción")
    st.write(f"**Etiqueta:** {class_names[class_id]}")
    st.write(f"**Confianza:** {confidence*100:.2f}%")
