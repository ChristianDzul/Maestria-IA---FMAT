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
| **1. GBFS** *(Greedy best-First Search)* |Oradea → Sibiu → Fagaras → Bucharest → Urziceni → Hirsova | 5 carreteras |644 Km | 5 nodos | success|
| **2. A\*** *(A Star Search)* | Oradea → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest → Urziceni → Hirsova |6 carreteras |612 km |9 nodos |success |

### `Calculo de heuristicas`

Utilizando la pareja `Oradea → Hirsova`, se pudo calcular las heuristicas desde la ciudad inicial a destino, obteniendo los siguientes resultados:

![alt text](/actividades/Imagenes/Heuristics_result.png)


### `1. Greedy Best-First Search (GBFS).`

Al ejecutar el algoritmo de busqueda Greedy, se obtuvierons los siguientes resultados. Como el destino no es Bucharest, la heuristica recurre automáticamente a la distancia euclidiana sobre las coordenadas aproximadas del mapa, en vez de la tabla AIMA. Esto se confirma corriendo 02_heuristics.py --from-city Oradea --to Hirsova, visto es los resultados previamente mostrados.

![alt text](/actividades/Imagenes/GBFS_result.png)

El subgrafo obtenido se puede observar de la siguiente manera:

![alt text](/actividades/Imagenes/GBFS_subgrafo.png)


### `2. A Star Search (A*).`

Al ejecutar el algoritmo de busqueda A*, se obtuvierons los siguientes resultados. Como en el caso previo haciendo uso del algoritmo Greedy, este tamnbien utiliza la distancia euclidiana.

![alt text](/actividades/Imagenes/A_star_result.png)

El subgrafo obtenido se puede observar de la siguiente manera:

![alt text](/actividades/Imagenes/A_Star_subrafo.png)


---

> ## 3. Conclusión


Con los resultados obtenidos, se se puede concluir que A* encontró el camino más óptimo com 612 km. por el contrario, Greedy se desvió, este devolvió una ruta de 644 km, 32 km más cara, aunque con una carretera menos. Greedy solo compara la heuristica h(n) qué tan "cerca en línea recta" se ve cada ciudad y nunca considera cuánto ya costó llegar hasta ahí, así que sacrificó costo real a cambio de parecer más cercano a la meta en cada paso.

Ahora bien, que h sea admisible solo garantiza que nunca sobreestima la distancia restante, es una propiedad necesaria para que A* sea óptimo, pero no le da ninguna garantía a Greedy, porque Greedy nunca usa g(n) en su decisión. El ejemplo concreto está en el propio recorrido: tras expandir Sibiu, la frontera tenía tanto Fagaras (h=249) como Rimnicu Vilcea (h=307); ambos algoritmos coincidieron y expandieron Fagaras primero (menor h). Pero al expandir Fagaras se genera Bucharest con h=136, siendo el valor más bajo visto hasta ese momento. Greedy salta inmediatamente a Bucharest porque tiene la h más chica de toda su frontera, sin notar que llegar ahí ya costó g=461 km. A* en cambio calcula `f = g + h` para ese mismo nodo Bucharest: f = 461 + 136 = 597, y como en su frontera todavía había nodos con f menor (Rimnicu Vilcea con f=538), A* pospone expandir esa rama y sigue explorando el camino vía Rimnicu Vilcea → Pitesti, que termina llegando a Bucharest con g=429 y f=565 más barato. 

Finalmente, f no tiende a disminuir a lo largo de la ruta en A*, por ejemplo; los valores de f a lo largo del camino final fueron 460 → 495 → 538 → 543 → 565 → 592 → 612, ahi se puede observar como este va incrementando. Esto es consecuencia directa de que la heurística usada es consistente, la distancia euclidiana entre dos ciudades nunca puede ser mayor que el costo real de la carretera que las conecta (la línea recta es, por definición, la distancia más corta posible). Cuando h es consistente, f nunca puede bajar de un nodo a su hijo, sin importar si el destino es Hirsova (heurística euclidiana, como aquí) o Bucharest (donde se usaría la tabla AIMA, documentada también como consistente). Esta propiedad es justamente la que permite que A* declare óptimo un nodo en cuanto lo saca de la frontera, sin tener que revisarlo después.

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