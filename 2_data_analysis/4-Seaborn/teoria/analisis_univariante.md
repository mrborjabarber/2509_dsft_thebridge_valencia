# Análisis Univariante

El **análisis univariante** es el método estadístico más básico y
fundamental dentro del análisis de datos. Como su nombre indica, se
centra únicamente en **una sola variable** a la vez, con el objetivo de
describir y comprender sus características principales, sin entrar en
relaciones con otras variables del conjunto de datos.

------------------------------------------------------------------------

## Objetivos del Análisis Univariante

1.  **Comprender la distribución de la variable**
    -   Observar si los valores se distribuyen de manera simétrica o
        sesgada.\
    -   Identificar si siguen un patrón particular (por ejemplo,
        distribución normal).
2.  **Medir la tendencia central**
    -   **Media**: el valor promedio de los datos.\
    -   **Mediana**: el valor central que divide a los datos en dos
        partes iguales.\
    -   **Moda**: el valor que aparece con mayor frecuencia.
3.  **Analizar la dispersión**
    -   **Rango**: diferencia entre el valor máximo y el mínimo.\
    -   **Varianza**: medida de la variabilidad de los datos respecto a
        la media.\
    -   **Desviación estándar**: dispersión promedio de los valores
        respecto a la media.
4.  **Detectar valores atípicos (outliers)**
    -   Aquellos puntos que se alejan significativamente del resto.\
    -   Son importantes porque pueden indicar errores, anomalías o casos
        especiales.

------------------------------------------------------------------------

## Técnicas y Herramientas Comunes

-   **Estadísticos descriptivos**: media, mediana, moda, rango,
    varianza, percentiles.\
-   **Gráficos**:
    -   **Histogramas**: muestran la frecuencia o densidad de los
        valores.\
    -   **Diagramas de caja (boxplots)**: útiles para detectar
        asimetrías y valores atípicos.\
    -   **Curvas de densidad (KDE)**: estimaciones suaves de la
        distribución.\
    -   **Gráficos de barras**: adecuados para variables categóricas.

------------------------------------------------------------------------

## Ejemplo Práctico

Imagina que tienes un conjunto de datos de Pokémon y estás interesado en
la variable **`Defense`**.

-   **Estadísticos**:
    -   Media: 65\
    -   Mediana: 60\
    -   Rango: 5 a 200
-   **Interpretación**:
    -   La mayoría de Pokémon tienen defensa alrededor de 60--70.\
    -   Existen algunos con defensas extremadamente altas que destacan
        como **outliers**.
-   **Visualización**:
    -   Un histograma permitiría ver la concentración de valores en el
        rango medio.\
    -   Un boxplot revelaría los valores atípicos en el extremo
        superior.

------------------------------------------------------------------------

## Importancia del Análisis Univariante

-   Es el **primer paso** en cualquier análisis exploratorio de datos
    (EDA).\
-   Ayuda a **detectar errores** en la base de datos (valores
    imposibles, nulos, inconsistentes).\
-   Proporciona un **resumen estadístico** sencillo pero poderoso de los
    datos.\
-   Permite **comprender mejor el contexto** antes de aplicar técnicas
    más complejas como análisis bivariantes o multivariantes.

------------------------------------------------------------------------

## Resumen

El análisis univariante consiste en **describir, resumir y visualizar
una variable por separado**.\
A través de estadísticas descriptivas y representaciones gráficas, se
obtiene una comprensión profunda del comportamiento de los datos,
identificando tendencias, patrones, variabilidad y posibles valores
atípicos.

------------------------------------------------------------------------

✍️ **En conclusión:**\
El análisis univariante es la base del análisis de datos, porque nos
enseña a conocer bien cada variable antes de relacionarla con otras. Es
una herramienta imprescindible para tomar decisiones informadas en
cualquier proceso de investigación, ciencia de datos o machine learning.
