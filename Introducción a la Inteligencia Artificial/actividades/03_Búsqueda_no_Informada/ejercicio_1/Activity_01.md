# Ejercicio 01 — Comparar BFS, UCS, DFS, DLS e IDS en el mapa de Rumania

**Materia:** Introducción a la Inteligencia Artificial
**Unidad / Módulo:** Búsqueda no informada
**Actividad:** Actividad 01
**Estudiante:** Christian Isaac Dzul Canul
**Programa:** Maestría en Inteligencia Artificial 🎓
**Docente:** Dr. Víctor Uc Cetina
**Fecha:** `04/09/2026`

---
> ## 1. Objetivo

Elegir una ruta distinta de Arad → Bucharest, correr BFS, UCS, DFS, DLS e IDS, y analizar diferencias de path, costo, profundidad y nodos expandidos.

---

> ## 2. Desarollo
El caso evaluado por default es la ruta **Arad → Bucharest**. Para esta actividad se fijara una nueva ruta quedando como `Oradea → Hirsova`, tomando como referencia el mapa de Romania (AIMA 3.2)  

![alt text](/actividades/Imagenes/Romania_map.png)


### Tabla comparativa

| Algoritmo | Path | Depth | Cost | Expanded | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. BFS** *(Breadth-First Search)* |Oradea → Sibiu → Fagaras → Bucharest → Urziceni → Hirsova | 5 carreteras |644 Km | 13 nodos | success|
| **2. UCS** *(Uniform-Cost Search)* |Oradea → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest → Urziceni → Hirsova |6 carreteras |612 km |15 nodos |success |
| **3. DFS** *(Depth-First Search)* |Oradea → Sibiu → Arad → Timisora → Lugoj → Mehadia → Drobeta → Craiova → Pitesti → Bucharest → Urziceni → Hirsova|11 carreteras |1207 km |12 nodos |success |
| **4. DLS** *(Depth-Limited Search)* | <ul><li>Con el --limit = 2 no se encuentra ningun path, cut off.</li><li> Con el --limit = 6 se obtiene el path: Oradea → Sibiu → Fagaras → Bucharest → Urziceni → Hirsova</li></ul>|5 carreteras |644 km | 16 nodos | success |
| **5. IDS** *(Iterative Deepening Search)* |Oradea → Sibiu → Fagaras → Bucharest → Urziceni → Hirsova |5 carreteras |644 km |36 nodos |success |

### `1. Breadth First Search (BFS).`

Al ejecutar BFS, se puede observar desde los resultados que:

<!-- <img src="/actividades/Imagenes/BFS_result.png" width="250" height="250"> -->

![alt text](/actividades/Imagenes/BFS_result.png)

El path obtenido, se observa de la siguiente manera:

![alt text](/actividades/Imagenes/BFS_Path.png)

### `2. Uniform Cost Search (UCS).`

Al ejecutar UCS, se puede observar desde los resultados que:

![alt text](/actividades/Imagenes/UCS_result.png)

El path obtenido, se observa de la siguiente manera:

![alt text](/actividades/Imagenes/UCS_path.png)


### `3. Depth First Search (DFS).`

Al ejecutar DFS, se puede observar desde los resultados que:

![alt text](/actividades/Imagenes/DFS_result.png)

El path obtenido, se observa de la siguiente manera:

![alt text](/actividades/Imagenes/DFS_path.png)


### `4. Depth Limited Search (DLS).`

Al ejecutar DLS con un limite igual a 2, se puede observar desde los resultados que:

![alt text](/actividades/Imagenes/DLS_result_1.png)

En cambio, cuando se establece un limite mayor, tal como es en este caso con **--limit 6**, entonces se obtiene lo siguiente:

![alt text](/actividades/Imagenes/DLS_result_2.png)

El path obtenido, se observa de la siguiente manera (--limit = 6):

![alt text](/actividades/Imagenes/DLS_path.png)


### `5. Iterative Deepening Search (IDS).`

Al ejecutar IDS, se puede observar desde los resultados que:

![alt text](/actividades/Imagenes/IDS_result.png)

El path obtenido, se observa de la siguiente manera:

![alt text](/actividades/Imagenes/IDS_path.png)

---

> ## 3. Conclusión

Como se puede observar en los resultados, utilizando la pareja `Oradea → Hirsova`, todos los algoritmos llegaron a una solución, pero con diferencias claras que ilustran justamente lo que cada uno optimiza.

En el caso de BFS, este devolvio el path con menos carreteras, siendo el path: **Oradea → Sibiu → Fagaras → Bucharest → Urziceni → Hirsova** con **5 carreteras**, siendo el minimo ya que expande nivel por nivel y garantiza el path con menos aristas (aunque no necesariamente el de menor km recorridos). En el caso contrario, UCS devolvió el path **Oradea → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest → Urziceni → Hirsova** con 6 carreteras pero solo 612 km. Esto confirma el comportamiento esperado, siendo que: BFS minimiza profundidad (aristas), UCS minimiza costo acumulado.

En cuanto a DFS, este no tiene ninguna noción de "cercanía" a la meta. simplemente sigue expandiendo el primer nodo no visitado (en este caso, en orden alfabético) hasta el fondo de una rama, y solo retrocede cuando se queda sin opciones. En la instancia obtenida, DFS bajó por la rama **Sibiu → Arad → Timisoara → Lugoj → Mehadia → Drobeta → Craiova → Pitesti** antes de llegar a Bucharest, resultando en un path de 11 carreteras y 1207 km, casi el doble de distancia que el de BFS o UCS. DFS no compara alternativas ni recuerda que existía una ruta más corta desde Sibiu directamente hacia Fagaras, una vez que entra a una rama, la agota por completo. Es completo pero no óptimo, ni en profundidad ni en costo.

Finalmente, en cuanto a DLS, Con **--limit 2** corta (cutoff) porque ninguna rama alcanza la meta en 2 pasos o menos. En cambio, Con **--limit 6** sí encuentra solución, y de hecho devuelve el mismo path de 5 carreteras que BFS: **Oradea → Sibiu → Fagaras → Bucharest → Urziceni → Hirsova**. Esto tiene sentido porque la profundidad real de la solución óptima en profundidad es 5 (la misma que reporta BFS), así que cualquier límite ≥ 5 es suficiente para encontrarla, y cualquier límite < 5 (como 2) es esperable que produzca cutoff. Precisamente por esto IDS, que va probando limit = 0, 1, 2, 3, 4, 5... hasta encontrar solución, converge también en el límite 5 y devuelve idéntico path, profundidad y costo que BFS (644 km, 5 carreteras). La diferencia está en el número de nodos expandidos: IDS repite trabajo en cada iteración (36 nodos generados en total, frente a los 13 expandidos de BFS), generando asi un costo extra a cambio de usar mucha menos memoria que BFS, ya que en cada iteración solo mantiene en memoria la rama actual en lugar de toda la frontera.

---
> ## 4. Criteria

1. La pareja origen–destino no es Arad → Bucharest.
2. Corriste BFS, UCS, DFS, DLS (con ≥ 2 límites) e IDS sobre esa misma pareja.
3. En tu reporte queda claro:
    - si BFS y UCS devolvieron el mismo path o no, y por qué;
    - si IDS coincide con BFS en profundidad (número de carreteras);
    - Qué pasó con DLS en el límite bajo (cutoff) frente al límite suficiente.
4. Incluyes evidencias (capturas o salida de terminal) de las corridas.