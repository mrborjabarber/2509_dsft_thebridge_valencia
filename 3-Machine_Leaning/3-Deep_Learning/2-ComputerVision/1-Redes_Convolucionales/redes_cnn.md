# Redes Neuronales Convolucionales (CNN) -- 

Una **red neuronal convolucional (CNN)** es un tipo de red neuronal
usada sobre todo para trabajar con **imágenes**, aunque también sirve
para audio y video.\
Piensa en ella como un *filtro inteligente* que aprende a detectar cosas
importantes dentro de una imagen: bordes, colores, formas, caras, etc.

------------------------------------------------------------------------

## 🧩 ¿Cómo funciona una CNN? 
Imagina que tienes una foto de un **gato** y quieres que la computadora
aprenda a reconocerlo.\
Una CNN pasa esa imagen por varios pasos:

### 1. **Convolución**

Es como pasar una lupa por toda la imagen, pero esta lupa no aumenta,
sino que detecta patrones.

**Ejemplo tonto:**\
Un filtro puede detectar solo **bordes verticales**.\
Si ve una línea vertical, dice: "¡Ajá, aquí hay algo interesante!".

### 2. **ReLU**

Es solo una función que convierte valores negativos en cero.\
Imagina que dice: "No quiero números tristes (negativos), solo positivos
:)".

### 3. **Pooling**

El *pooling* se encarga de **hacer la imagen más pequeña**, manteniendo
lo importante.

Hay dos tipos:

#### 🔹 Max Pooling (el más usado)

Se queda solo con el número más grande de una zona.

**Ejemplo muy tonto:**

Si en un cuadrado tienes:

    1 5
    3 2

El *max pooling* dice:\
"Quiero el más grande → **5**".

Esto hace que la red: - trabaje más rápido\
- ignore detalles irrelevantes\
- se enfoque en lo que realmente importa

#### 🔹 Average Pooling

Saca el promedio de los valores.\
Es menos usado hoy en día.

------------------------------------------------------------------------

## 🧠 4. Capas completamente conectadas (Fully Connected Layers)

Al final, después de todos los filtros y poolings, la red junta toda la
información y decide:

"¿Es un gato? ¿Un perro? ¿Un auto? ¿Una tostadora?"

------------------------------------------------------------------------

# 🎯 Ejemplo completo y simple

Supón que una CNN ve esta imagen:

🐱 → detecta orejas, ojos, bigotes\
🎯 "Esto parece un gato"

Luego otra capa dice:\
📦 "Confirmado, características de gato encontradas"

Y al final:\
🧠 **Salida:** "Gato (95% de confianza)"

------------------------------------------------------------------------

# 📝 Resumen:

-   Una CNN **analiza imágenes** paso a paso.\
-   La **convolución** encuentra patrones.\
-   El **pooling** reduce la imagen conservando lo importante.\
-   Las capas finales **deciden qué es la imagen**.\
-   Sirve para **reconocimiento facial**, autos autónomos, filtros de
    TikTok, etc.

------------------------------------------------------------------------


