# Ejercicio 01 — Comparar Greedy y A* en el mapa de Rumania

**Materia:** Introducción a la Inteligencia Artificial
**Unidad / Módulo:** Búsqueda informada
**Actividad:** Actividad 01
**Estudiante:** Christian Isaac Dzul Canul
**Programa:** Maestría en Inteligencia Artificial 🎓
**Docente:** Dr. Víctor Uc Cetina
**Fecha:** `06/09/2026`

---
> ## 1. Objetivo

Elegir una ruta distinta de Arad → Bucharest, inspeccionar h(n), correr Greedy y A*, y analizar diferencias de camino, costo, profundidad y nodos expandidos a la luz de g, h y f.

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


El path obtenido, se observa de la siguiente manera:





---

> ## 3. Conclusión



---
> ## 4. Criteria

- La pareja origen–destino no es Arad → Bucharest.
- Corriste Greedy y A* sobre esa misma pareja.
- Consultaste 02_heuristics.py para el mismo destino.
- En tu reporte queda claro:
    - si Greedy y A* devolvieron el mismo camino o no, y por qué;
    - qué heurística se usó (tabla AIMA vs. euclidiana);
    - en al menos un punto de decisión, cómo h(n) (Greedy) frente a f(n) = g(n) + h(n) (A*) explica la ciudad que cada algoritmo expandió.
- Incluyes evidencias (capturas o salida de terminal) de las corridas.