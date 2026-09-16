# Ejercicio 01 — Separar los blobs y volver a elegir (k)

**Materia:** Introducción a la Inteligencia Artificial
**Unidad / Módulo:** Clustering K-medias
**Actividad:** Actividad 01
**Estudiante:** Christian Isaac Dzul Canul
**Programa:** Maestría en Inteligencia Artificial 🎓
**Docente:** Dr. Víctor Uc Cetina
**Fecha:** `13/09/2026`

---

> ## 1. Objetivo

Correr la notebook en Colab tal como está, anotar el (k) que sugieren codo y silueta, separar los 5 blobs en el arreglo blob_centers (y, si hace falta, blob_std) y volver a graficar. Debes ver si el codo y la silueta se mueven hacia (k = 5).

---

> ## 2. Desarollo



###  `Codigo original`

Los resultados obtenidos en la ejecucion origianl fueron los siguientes:

- Scatterplot (blobs):

![alt text](/actividades/Imagenes/Scatterplot_original.png)

- Diagrama de Voronoi (k=5)

![alt text](/actividades/Imagenes/Voronoi_original.png)

- Curva de Inercia (codo)

![alt text](/actividades/Imagenes/codo_original.png)

- Curva de silueta

![alt text](/actividades/Imagenes/silueta_original.png)


## `Codigo Editado`

Los resultados obtenidos en la ejecucion origianl fueron los siguientes:

- Scatterplot (blobs):

![alt text](/actividades/Imagenes/Scatterplot_modificado.png)

- Diagrama de Voronoi (k=5)

![alt text](/actividades/Imagenes/Voronoi_modificado.png)

- Curva de Inercia (codo)

![alt text](/actividades/Imagenes/Codo_modificado.png)

- Curva de silueta

![alt text](/actividades/Imagenes/silueta_modificado.png)


- Valores comparativos entre inercias del codigo original y el modificado:

![alt text](/actividades/Imagenes/Kmeans_results.png)

Para mayor detalle, se puede ver los resultados en la ruta: [01 K-medias.ipynb](/actividades/07_Clustering_K_medias/Notebooks/01%20K-medias.ipynb)



El codo prefiere que K sea igual a 4 porque tres de los cinco blobs comparten la misma $x=-2.8$ (aunque con `std=0.1`, cada uno por separado sí es compacto) y quedan alineados verticalmente muy cerca unos de otros, formando visualmente una sola región alargada. Al bajar de $k=5$ a $k=4$, K-Means fusiona dos de esos tres blobs verticales en un solo clúster y la inercia casi no sube, mientras que bajar de $k=4$ a $k=3$ por ejemplo sí duele mucho. Por eso el "codo", el punto donde añadir más clústeres deja de bajar mucho la inercia, cae en $k=4$ y no en $k=5$: para K-Means, tres blobs alineados valen casi lo mismo que dos.

Ahora bien, con los codos separados al dar a los tres blobs de la izquierda una $x$ distinta cada uno (y subir su `std` de 0.1 a 0.2), la inercia baja fuerte hasta $k=5$ y luego se aplana. El codo queda claramente en $k=5$. La silueta confirma lo mismo: su máximo pasa de estar en $k=4$ a estar en $k=5$, y ahora sí es el pico más alto de toda la curva. Codo y silueta coinciden en $k=5$.

Finalmente, si el codo sigue en 4 es necesario mover inicialmente la **distancia entre centros**, no tanto `blob_std`. Ya que por ejemplo, dos blobs se ven como uno solo cuando su distancia es menor entre si. Si el codo se quedara en $k=4$ después de separar los centros, valdría la pena revisar primero si esa distancia sigue siendo menor que ese umbral para algún par de blobs (en cuyo caso hay que alejarlos más en $x$ o en $y$); solo si los centros ya están razonablemente lejos y el problema persiste tendría sentido *bajar* `blob_std` (nunca subirlo, porque subir la dispersión sin alejar los centros es lo que vuelve a pegar a los blobs).

---
> ## 4. Criteria

- La notebook original corrió en Colab (no solo en tu máquina).
- Los centros no son los de Géron; en el scatter se distinguen cinco nubes (aunque alguna se solape un poco).
- Sigues teniendo 5 centros y 2000 puntos.
- Hay capturas antes y después del scatter, del codo y de la silueta.
- El reporte dice con números (inercias o scores) si el codo / la silueta se acercaron a (k = 5); no basta “se ve mejor”.