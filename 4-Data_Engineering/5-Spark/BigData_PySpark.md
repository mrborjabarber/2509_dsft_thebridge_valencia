# Big Data

Big Data se refiere al manejo y análisis de grandes volúmenes de datos que no pueden ser procesados eficientemente con herramientas tradicionales. Sus características principales son:

## Volumen
Cantidad masiva de datos que requiere sistemas distribuidos para su almacenamiento y procesamiento.

## Velocidad
Los datos se generan rápidamente y necesitan ser procesados en tiempos reducidos, a veces en tiempo real.

## Variedad
Los datos provienen en distintos formatos: estructurados, semiestructurados y no estructurados.

# PySpark

PySpark es la interfaz de Python para Apache Spark, un motor de procesamiento distribuido diseñado para trabajar con grandes cantidades de datos de forma eficiente. Permite distribuir tareas entre múltiples máquinas dentro de un cluster.

PySpark se utiliza para:
- Procesamiento masivo de datos (ETL)
- Análisis de datos distribuidos
- Machine Learning a gran escala mediante MLlib
- Procesamiento de datos en streaming

# Clusters en Big Data y PySpark

Un cluster es un conjunto de computadoras que trabajan coordinadamente como un solo sistema para procesar datos de manera distribuida. Su objetivo principal es dividir el procesamiento en múltiples nodos para obtener mayor velocidad y capacidad.

## Componentes de un cluster

### Nodo Maestro (Master Node)
Coordina el funcionamiento del cluster, administra los recursos y asigna tareas. Es donde se ejecuta el driver de Spark.

### Nodos Trabajadores (Worker Nodes)
Son las máquinas encargadas de ejecutar las tareas asignadas. Cada una contiene procesos llamados executors que procesan los datos de forma paralela.

### Cluster Manager
Sistema que administra los recursos del cluster. Spark puede trabajar con sistemas como:
- Standalone
- YARN
- Mesos
- Kubernetes

# Funcionamiento del procesamiento distribuido

1. El programa PySpark envía el trabajo al driver.
2. El driver coordina con el cluster manager la distribución de recursos.
3. Las tareas se reparten entre los nodos trabajadores.
4. Cada worker procesa una parte de los datos en paralelo.
5. Los resultados se combinan y se devuelven al driver.
