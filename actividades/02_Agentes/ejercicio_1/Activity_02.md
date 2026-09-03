# Ejercicio 02 — Cambiar la ubicación del Wumpus y los pits

**Materia:** Introducción a la Inteligencia Artificial
**Unidad / Módulo:** Conceptos básicos de Inteligencia Artificial
**Actividad:** Actividad
**Estudiante:** Christian Isaac Dzul Canul
**Programa:** Maestría en Inteligencia Artificial 🎓
**Docente:** Dr. Víctor Uc Cetina
**Fecha:** `31/08/2026`

---
> ## 1. Objetivo

Crear una nueva configuración modificando la posición del Wumpus y de los pits, respetando las reglas del entorno, y analizar el efecto sobre los distintos agentes.

---

> ## 2. Desarollo

1. **Paso 1:** Generación de una nueva cueva/mapa.

   Para empezar, se generó una nueva cueva previo a hacer uso de los agentes. Este tiene el nombre `mi_cueva_4x4.yaml`. El mapa original se ve de esta manera:

   ![alt text](/actividades/Imagenes/OriginalMap.png)

   Ahora bien, para el nuevo mapa `mi_cueva_4x4.yaml`, tras realizar las modificaciones, termino luciendo:

   ![alt text](/actividades/Imagenes/NewMap.png)

   Y con los siguientes valores:

   ```yaml

   grid:
   width: 4
   height: 4

   agent:
   start: [1, 1]
   direction: east
   arrows: 1

   wumpus: [2, 2]

   pits:
   - [1, 4]
   - [3, 4]
   - [4, 1]

   gold: [4, 3]

   scoring:
   gold: 1000
   death: -1000
   step: -1
   shoot: -10

   max_steps: 200

   
1. **Paso 2:** Prueba de los diferentes agentes usando el mapa nuevo.

      - Simple reflex agent:

         Los resultados que se obtuvieron fueron los siguientes:

         ![alt text](/actividades/Imagenes/Simple_reflex_result.png)

         Se puede observar que si bien si se movio de su posicion inicial, pasando de (1,1) a (2,1), este quedó ciclado cambiando únicamente su dirección sin moverse de su posición y alcanzando el numero máximo de steps sin destrabasrse, esto debido a que no tiene la capacidad de recordar si el camino recorrido es seguro.

      - Model based agent:

         Los resultados que se obtuvieron fueron los siguientes:

         ![alt text](/actividades/Imagenes/model_based_result.png)

         Sin embargo, para ver qué pasa justo antes de quedarse trabado, bajé las iteraciones a 20. Ahí se nota que al principio el agente gira y avanza hacia el norte, llegando a (2,2), detecta el hedor del Wumpus y como no tiene manera de saber si seguir es seguro, se regresa a la casilla inicial (1,1) para probar otra ruta. Pero cuando se vuelve a topar con el hedor por el nuevo camino, por las propias limitaciones de este tipo de agente, termina quedándose rotando en lugar de arriesgarse a moverse a otra casilla

         ![alt text](/actividades/Imagenes/model_based_res2.png)


      - Goal based agent:

         Los resultados que se obtuvieron fueron los siguientes:

         ![alt text](/actividades/Imagenes/goal_based_result.png)
   
         Aquí pasa algo muy similar al `agente model-based`, pero por razones distintas. A diferencia del anterior, este sí mapea las rutas posibles y las evalúa según su nivel de seguridad o riesgo.

         Primero va hacia el norte, detecta hedor y frena porque ve que las casillas de al lado son peligrosas. Por eso, retrocede para probar por otro lado, pero vuelve a percibir hedor. Al ver que ya no le quedan caminos seguros que lo acerquen al oro, se queda atrapado girando en su última posición.

         Ademas, como el agente no puede determinar con absoluta certeza una única celda donde esté el Wumpus, sino que, al llegar a (2,1) sospecha que podría estar en (2,2) o en (3,1), por lo que no dispara para despejar el camino.

      - Utility based agent:

         Los resultados que se obtuvieron fueron los siguientes:

         ![alt text](/actividades/Imagenes/Utility_based_result.png)

         Este modelo sigue patrones similares al `agente goal-based` con la diferencia de que su arquitectura evalua el costo de los diferentes caminos y pasos a tomar, tomando en cuenta los valores de penalizacion o costo, y la probabilidad de que ocurra un evento (encontrarse con el wumpus, pit, u oro), esto con el fin de tomar el camino que considere más optimo tomando los riesgos necesarios. Es por ello que decide arriesgarse y muere.


      - Learning agent: 

         Los resultados que se obtuvieron fueron los siguientes:

         ![alt text](/actividades/Imagenes/Learning_agent_result.png)

         A diferencia de los modelos anteriores, este usa las mejores caracteristicas de cada uno e implementa un sistema de recompensas y retroalimentacion para enseñar al agente cuando toma una opcion incorrecta (penaliza) y cuando una que es correcta (recomepensa). Usando cierto numero de iteraciones, este toma lo aprendido y lo implementa para resolver el problema. En este caso, se puede observar que con las 1500 iteraciones el agente consiguó identificar un camino para conseguir el oro y salir a salvo.
---

> ## 3. Conclusión


   Para concluir, para la configuración presentada en `mi_cueva_4x4.yaml`, el único agente capaz de finalizar el mapa fue el `learning agent`, mientras que el resto no, tal como lo podemos observar en las evidencias y resultados obtenidos de los demas agentes. Adicionalmente, el `Simple reflex agent` es el que peor desempeño tuvo devido a sus limitaciones y capacidades de no recordar las casillas que visitó, quedandose estancado girando a la derecha hasta llegar al máximo numero de iteraciones. Asi mismo, el `model based agent` al jugar con los pit de manera que los acerques o alejes, este adopta un comportamiento similar a cuando se encuentra con el wumpus, de manera que no se mueve en dirección de casillas que pudieran ser posiblemente riesgosas, y por lo tanto, se queda girando.
   
---
> ## 4. Criteria

1. config/mi_cueva_4x4.yaml carga sin errores de validación.
2. El Wumpus y los pits están en posiciones distintas a las del mapa clásico.
3. Existe un camino seguro de ida y vuelta al oro (algún agente lo demuestra saliendo con puntaje positivo).
4. El mapa cumple todas las reglas de validez.