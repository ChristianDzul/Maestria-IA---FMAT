# Ejercicio 01 — Más capas en el perceptrón multicapa (Iris)

**Materia:** Introducción a la Inteligencia Artificial
**Unidad / Módulo:** Perceptrón multicapa
**Actividad:** Actividad 01
**Estudiante:** Christian Isaac Dzul Canul
**Programa:** Maestría en Inteligencia Artificial 🎓
**Docente:** Dr. Víctor Uc Cetina
**Fecha:** `08/09/2026`

---

> ## 1. Objetivo

Correr ambas notebooks en Google Colab con la arquitectura original, agregar dos capas a cada red, volver a entrenar y comparar qué cambia (curva de error/pérdida, velocidad, calidad de la clasificación).

---

> ## 2. Desarollo

###  `Multilayer perceptron`

#### **Primer ejecución (original)**

Es importante considerar, la primera ejecución se constituye con una estructura o topologia de 4 entradas, una capa oculta de 3 neuronas, y 3 neuronas de salida. Para ello se hace uso de la activacion sigmoide y calculo del error mediante MSE. Los resultados obtenidos fueron:

![alt text](/actividades/Imagenes/MLP_result.png)


#### **Segunda ejecución (Profunda)**

Se conservaron las mismos métodos, con la excepción de que se añadieron 2 capas más, y se ajustaron las funciones para la inicialización de pesos en las capas, calculo de error, propagación y retropropagación de los errores.

![alt text](/actividades/Imagenes/MLP_prof_result.png)


Para mayor detalle, se puede ver los resultados en la ruta: [04_Multilayer_perceptron_result.ipynb](/actividades/05_Perceptrón_multicapa/Notebooks/04_Multilayer_perceptron_result.ipynb)

---

###  `Keras - multilayer perceptron - iris` 

#### **Primer ejecución (original)**

Es importante considerar, la primera ejecución se constituye con una estructura diferente a la previa ya que se usa tensor flow para Keras, aunque conserva la misma topologia (4 x 3 x 3)

Model summary:

![alt text](/actividades/Imagenes/Model_summ_1.png)

Results (loss y curve loss):

![alt text](/actividades/Imagenes/KMLP_result_1.png)


#### **Segunda ejecución (Profunda)**

Se conservaron las mismos métodos, con la excepción de que se añadieron 2 capas más.

Model summary:

![alt text](/actividades/Imagenes/Model_summ_2.png)

Results (loss y curve loss):

![alt text](/actividades/Imagenes/KMLP_result_2.png)

Para mayor detalle, se puede ver los resultados en la ruta: [05 Keras - multilayer perceptron - iris.ipynb](/actividades/05_Perceptrón_multicapa/Notebooks/05_Keras_multilayer_perceptron_result.ipynb)


---

> ## 3. Conclusión y resultados

**Configuración común en las 4 corridas:** activación sigmoide en todas las capas, error MSE, SGD con alpha = 0.03, 500 épocas.

## Tabla comparativa

| Implementación | Topología| Error/Loss final | Comportamiento de la curva |
|---|---|---|---|
| NumPy (manual) | 4×3×3 | poco menor a 0.1  | Descenso continuo y sostenido durante las 500 épocas |
| NumPy (manual) | 4×3×3×3×3 | menor a 0.6 | Caída abrupta en las primeras épocas, luego estancamiento total tomando una forma de "L" |
| Keras | 4×3×3 (2 `Dense`) |0.1852 | Descenso continuo sostenido aunque algo lento durante las 500 épocas, por lo que no se observa tan curvo y ni una bajada rápida |
| Keras | 4×3×3×3×3 (4 `Dense`) |0.2220 | Caída inicial rápida, luego estancamiento con leves oscilaciones que visualmente no se observan pero se ve en el loss atraves de las epocas|


Em ambas implementaciones el error **empeoró** al añadir las dos capas extra, y el patrón es el mismo en las dos: caída inicial rápida seguida de **estancamiento** prolongado a lo largo del resto de epocas hasta alcanzar las 500. En NumPy el efecto es más severo (el error final de la red profunda, menor a 0.6 aproximandamente, es más de 10 veces el de la original, poco menor a 0.1 ), mientras que en Keras la diferencia es más moderada (0.2220 vs 0.1852) pero la tendencia profunda es mucho mayor que en la original.

Ahora bien, Las curvas de NumPy y Keras se parecen con la misma topología. En ambas implementaciones la red original converge de forma estable a traves de las epocas, y la profunda cae rápido al inicio para luego estancarse. Sin embargo, en NumPy el estancamiento de la red profunda es mucho más severo en comparación que en Keras. Esto puede deberse a:

- **Inicialización de pesos distinta** ya que en NumPy este usa una distribución uniforme simple entre -0.5 y 0.5 sin escalar por el tamaño de la capa, mientras que Keras usa por defecto Glorot/Xavier, que probablente ayude  a mitigar en algo el desvanecimiento del gradiente.

- **Orden y agrupamiento de actualización de pesos** , si bien ambos usan SGD, estos lo procesan de manera inter, causando un diferente resultado.

Con respecto a las sigmoides y el MSE. Apilar sigmoides, cada capa introduce un factor de derivada `output×(1-output)` (máximo 0.25) en el gradiente que se retropropaga. Por lo que es esperable que con 4 capas, el gradiente que llega a las primeras capas es el producto de hasta 4 de estos factores, reduciéndose a una fracción muy pequeña de su valor original, observando que el **gradiente se desvanece**. Esto explica la forma de la repentina caida observada en ambas implementaciones, por lo que se puede deducir que las primeras capas reciben una mejor gradiente para un ajuste inicial rápido, pero el resto de capas reciben una señal o peor gradiente demasiado débil para seguir aprendiendo, y el entrenamiento se estanca. Además, tambien entra en juego factores como la complejidad y data con la que se cuente, ya que se puede dar el caso en el que tener mas profundidad o capas estan demas, y que inclusive entorpezca la propagación del gradiente como lo fue en este caso.


En conclusión, agregar dos capas ocultas no solo no mejoró el aprendizaje sino que lo perjudicó, de forma consistente en la implementación manual y en Keras. Esto confirma que la profundidad debe ir acompañada de ajustes (activaciones como ReLU, pérdida como cross-entropy, mejor inicialización) para no verse dominada por el desvanecimiento del gradiente, y que en problemas simples como Iris, más capas no implican mejor desempeño.

---
> ## 4. Criteria

- Las dos notebooks originales corrieron en Colab (no solo en tu máquina).
- Cada red profunda tiene dos capas extra; la salida sigue siendo de 3 neuronas.
- La notebook 01 actualiza forward y backprop (no solo la inicialización).
- Hay evidencias (capturas) de las cuatro corridas: curvas y, en Keras, model.summary() original y profundo.
- El reporte compara implementación a mano vs. Keras y red original vs. red más profunda; no es un resumen de lo que “debería” pasar sin números.