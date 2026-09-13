# Ejercicio 01 — Cambiar la imagen de predicción en YOLO

**Materia:** Introducción a la Inteligencia Artificial
**Unidad / Módulo:** Visión computacional
**Actividad:** Actividad 01
**Estudiante:** Christian Isaac Dzul Canul
**Programa:** Maestría en Inteligencia Artificial 🎓
**Docente:** Dr. Víctor Uc Cetina
**Fecha:** `10/09/2026`

---

> ## 1. Objetivo

Correr la notebook en Colab tal como está, sustituir las dos imágenes de muestra por una imagen tuya (la misma en ambas predicciones) y comparar qué objetos detecta YOLO en la foto original frente a la tuya.

---

> ## 2. Desarollo

Para la ejecución del notebook, se tiene seleccionado el runtime haciendo uso de la GPU: **"T4 GPU"** para el entorno.

![alt text](/actividades/Imagenes/runtime.png)

###  `Codigo original`

Para la prediccion, se utiliza la imagen de zidane, una vez ejecutada podemos ver la imagen resultante. En `zidane.jpg` el modelo detectó **2 personas** (con confianza 0.84 y 0.82) y **1 corbata** (con confianza 0.29). 

![alt text](/actividades/Imagenes/Zidane_result.png)

Ahora bien, en cuanto a la imagen del `bus.jpg` el modelo detectó **4 personas, 1 autobús (`bus`) y 1 señal de alto (`stop sign`)**.

![alt text](/actividades/Imagenes/Bus_result.png)


## *`Codigo Editado

 En mi foto propia (`Cdmx_viaje.jpeg`, una escena urbana en la CDMX) el modelo detectó únicamente dos clases de COCO presentes en la imagen: **`person`** (1 persona aunque la señala 2 veces, confianza 0.61) y **`car`** (5–8 autos segun el modelo, aunque en la imagen se observan unicamente 5 de las cuales no marca 1 de ellas siendo el camion del fondo a la izquierda, con confianzas ligeramente diferentes usando el CLI y modelo, dando valores entre 0.58 y 0.89).

![alt text](/actividades/Imagenes/Miimagen_result2.png)

![alt text](/actividades/Imagenes/Mi_imagen_result_1.png)

Hay varios elementos visualmente claros que YOLO no etiquetó siendo algunos como el **edificio** de fondo, los **árboles y arbustos**, y el **poste de luz** a la derecha. La razón principal es que ninguna de esas clases existe en el dataset COCO ya que estan orientadas a personas, vehículos, animales y objetos cotidianos, sin clases de "edificio", "árbol" o "poste". Además, uno de los autos del extremo derecho aparece cortado por el borde del encuadre debido al árbol, lo que reduce la confianza de su detección (0.45), y la persona está parcialmente **ocluida, lo que también baja su score.

Ahora bien, como mencione anteriormente, las predicciones utilizando el CLI y la del model (...) a pesar de utilizar la mismas imagenes para ambas estos no coinciden exactamente, aunque son muy similiares. Ambas detectan 2 personas, pero difieren en el conteo de autos con ligeras variaciones en las confianzas de las mismas cajas (p. ej. el auto principal pasa de 0.89 a 0.83). Esto no se debe a que sean modelos distintos, sino a que, en el flujo editado, antes de correr `model('/content/Cdmx_viaje.jpeg')` se ejecuta `model.train(data='coco128.yaml', epochs=3)` sobre ese mismo objeto `model`. Ese entrenamiento adicional (aunque breve, 3 épocas) modifica ligeramente los pesos, por lo que la inferencia posterior ya no corresponde al YOLOv8n original, sino a una versión ajustada, por lo que se pueden ver pequeñas variaciones entre ambas predicciones.

Para mayor detalle, se puede ver los resultados en la ruta: [013 YOLO ultralytics.ipynb](/actividades/06_Visión_computacional/ejercicio_1/Notebook/13_YOLO_ultralytics.ipynb)

---
> ## 4. Criteria

- La notebook original corrió en Colab (no solo en tu máquina).
- El único cambio de código es la fuente de la imagen en las dos predicciones; el modelo sigue siendo yolov8n.pt.
- Tu imagen no es zidane.jpg ni bus.jpg.
- Hay capturas de las predicciones originales y de la tuya, con cajas visibles.
- El reporte nombra clases concretas (no basta “detectó cosas”).