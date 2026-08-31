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

1. **PASO 1:** Generación de una nueva cueva/mapa.

   Para empezar, se genero una nueva cueva previo a hacer uso de los agentes. Este tiene el nombre `mi_cueva_4x4.yaml`. El mapa original se ve de esta manera:

   ![alt text](/actividades/Imagenes/OriginalMap.png)

   Ahora bien, para el nuevo mapa `mi_cueva_4x4.yaml`, tras realizar las modificaciones, termino luciendo:

   ![alt text](/actividades/Imagenes/NewMap.png)


---

> ## 3. Criteria

1. config/mi_cueva_4x4.yaml carga sin errores de validación.
2. El Wumpus y los pits están en posiciones distintas a las del mapa clásico.
3. Existe un camino seguro de ida y vuelta al oro (algún agente lo demuestra saliendo con puntaje positivo).
4. El mapa cumple todas las reglas de validez.