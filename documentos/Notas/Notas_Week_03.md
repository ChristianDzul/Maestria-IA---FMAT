> ### Fecha: `[07/09/2026]`

####  📌 Notas y Hallazgos (Día 08):

### Clustering K-medias

El **Clustering de K-medias (K-means)** es una de las técnicas más populares del **aprendizaje no supervisado**, la cual se utiliza para encontrar estructuras o patrones ocultos en datos que no están etiquetados [1-3]. Su objetivo principal es dividir un conjunto de datos en **grupos naturales llamados "clusters"**, de tal manera que los elementos dentro de un mismo grupo sean muy similares entre sí y muy diferentes a los de otros grupos [2, 3].

A continuación, se explica su funcionamiento de manera completa y sencilla:

### 1. ¿Qué es el "K" y qué son las "Medias"?
*   **La "K":** Representa el número de grupos o clusters que deseas crear [4, 5]. Es un número entero positivo que el usuario debe definir antes de iniciar el algoritmo [6, 7].
*   **Las "Medias" (Centroides):** Son el "corazón" del algoritmo [4, 8]. Cada grupo tiene un punto central llamado **centroide**, que representa el promedio (la media) de todos los puntos asignados a ese grupo [8-10].

### 2. ¿Cómo funciona el algoritmo? (Paso a paso)
El proceso es iterativo, lo que significa que el algoritmo repite los mismos pasos varias veces hasta que los grupos se estabilizan [4, 8, 11]:

1.  **Elección de K:** Se decide cuántos grupos se quieren formar [6].
2.  **Selección inicial:** Se eligen *k* puntos al azar como los centroides iniciales [6, 12].
3.  **Asignación de puntos:** Se calcula la **distancia** (generalmente la distancia Euclidiana) entre cada dato y cada centroide [4, 6, 12]. Cada dato se asigna al cluster cuyo centroide esté más cerca [6, 11].
4.  **Actualización de centroides:** Una vez que todos los datos tienen un grupo, se calcula una nueva posición para cada centroide promediando la ubicación de todos los puntos asignados a él [9-11].
5.  **Repetición:** Los pasos 3 y 4 se repiten una y otra vez hasta que **convergen**; es decir, hasta que ningún dato cambie de grupo de una repetición a otra [9-11, 13].

### 3. ¿Cómo elegir el número correcto de grupos (K)?
Dado que el usuario debe proporcionar el valor de *k*, una técnica común para encontrar el número óptimo es el **Método del Codo (Elbow Method)** [14]. Consiste en graficar el número de clusters frente a la varianza de los datos; el punto donde la curva se dobla bruscamente (como un codo) sugiere la cantidad ideal de grupos para ese conjunto de datos [14].

### 4. Ventajas y Limitaciones
*   **Ventajas:** Es un algoritmo sencillo de entender, rápido de procesar y muy efectivo para grandes volúmenes de datos [4, 15].
*   **Limitaciones:** 
    *   Requiere que el usuario defina *k* de antemano, lo cual puede ser difícil si no conoces bien los datos [7].
    *   Es sensible a los **valores atípicos (outliers)**, que pueden deformar los promedios [16].
    *   Tiende a crear clusters de forma circular; si los datos tienen formas alargadas o elípticas, el algoritmo puede tener dificultades para agruparlos correctamente en comparación con otros métodos como GMM (Modelos de Mezcla Gaussiana) [17].

**Ejemplo práctico:** Imagina que tienes una mezcla de imágenes de perros y gatos sin etiquetas [2, 18]. El algoritmo de K-medias analizará características como la forma de las orejas o el tamaño, y separará las fotos en dos grupos basados en sus similitudes visuales, incluso sin saber qué es un "perro" o un "gato" [2, 18].

¿Te gustaría que generemos una **infografía** o una **guía de estudio** que resuma visualmente este proceso y lo compare con otros tipos de clustering?