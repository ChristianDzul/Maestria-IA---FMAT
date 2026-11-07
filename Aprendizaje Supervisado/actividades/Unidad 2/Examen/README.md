# Examen Módulo 2 — Predicción de la estabilidad de una red eléctrica

**Notebook:** `Dzul_Christian_Examen_Modulo2.ipynb`
**Materia:** Aprendizaje Supervisado — Módulo 2 (Regresión)

Este README explica, sección por sección, qué hace el notebook, por qué lo hace y qué instrucción de la práctica cumple cada parte. Está escrito para alguien que nunca ha trabajado con estos temas, así que primero define los conceptos básicos.

---

## Índice

1. [¿De qué trata el problema?](#1-de-qué-trata-el-problema)
2. [Conceptos básicos antes de empezar](#2-conceptos-básicos-antes-de-empezar)
3. [Mapa: instrucciones de la práctica → secciones del notebook](#3-mapa-instrucciones-de-la-práctica--secciones-del-notebook)
4. [Cómo ejecutar el notebook](#4-cómo-ejecutar-el-notebook)
5. [Recorrido sección por sección](#5-recorrido-sección-por-sección)
6. [Resumen de resultados](#6-resumen-de-resultados)
7. [Preguntas frecuentes](#7-preguntas-frecuentes)
8. [Glosario](#8-glosario)

---

## 1. ¿De qué trata el problema?

Una **red eléctrica inteligente** de cuatro nodos (un productor de energía y tres consumidores) puede ser **estable** (sigue funcionando bien ante cambios) o **inestable** (los cambios se amplifican). El conjunto de datos contiene 10,000 simulaciones de esa red; cada una tiene:

| Columnas | Significado |
|---|---|
| `tau1`–`tau4` | Tiempo de reacción de cada nodo ante un cambio en la red |
| `p1`–`p4` | Potencia generada (`p1`, positiva) o consumida (`p2`–`p4`, negativas). Por balance: `p1 = -(p2 + p3 + p4)` |
| `g1`–`g4` | Elasticidad del precio: qué tanto reacciona cada nodo a cambios de precio |
| **`stab`** | **Lo que queremos predecir**: margen de estabilidad. Negativo = estable; positivo = inestable |

Como `stab` es un **número continuo** (no una categoría), el problema es de **regresión**.

**Los archivos:**

| Archivo | Filas | ¿Tiene `stab`? | Uso |
|---|---|---|---|
| `electrical_grid_stability_train.csv` | 8,000 | Sí | Entrenar los modelos y elegir sus parámetros con validación cruzada |
| `electrical_grid_stability_test.csv` | 2,000 | No | Lo conserva el profesor; con él se generan las predicciones finales |

> **Nota:** el archivo de prueba **no se entrega al alumno a propósito**. Así se garantiza que ninguna decisión del modelo se tome mirando los datos con los que se va a evaluar.

---

## 2. Conceptos básicos antes de empezar

### 2.1 ¿Qué es un modelo de regresión?

Es una función que recibe las variables de entrada (`tau`, `p`, `g`) y devuelve un número: la predicción de `stab`. El modelo **aprende** esa función a partir de ejemplos donde sí conocemos la respuesta correcta.

### 2.2 ¿Cómo se mide qué tan bueno es?

Comparando la predicción con el valor real. La diferencia se llama **residuo** (`real − predicho`). Con los residuos se calculan tres métricas:

| Métrica | Qué significa | Mejor valor |
|---|---|---|
| **RMSE** (raíz del error cuadrático medio) | Error típico, en las mismas unidades que `stab`. Castiga más los errores grandes. **Es la métrica principal del examen.** | Lo más bajo posible |
| **MAE** (error absoluto medio) | En promedio, por cuánto se equivoca el modelo | Lo más bajo posible |
| **R²** | Qué fracción de la variación de `stab` explica el modelo. 1 = perfecto; 0 = igual que predecir siempre el promedio | Lo más cercano a 1 |

> **¿Y el accuracy?** El *accuracy* (exactitud) se usa en **clasificación**, cuando la respuesta es una categoría. Aquí `stab` es un número, así que se usan RMSE, MAE y R².

### 2.3 Subajuste y sobreajuste

- **Subajuste:** el modelo es demasiado simple y se equivoca mucho incluso con los datos con los que aprendió.
- **Sobreajuste:** el modelo es tan flexible que **memoriza** los datos de entrenamiento (incluido su ruido) y falla con datos nuevos.

Para detectarlo comparamos dos errores:

| Error de entrenamiento | Error de validación | Diagnóstico |
|---|---|---|
| Alto | Alto (parecido) | Subajuste |
| Bajo | Bajo (parecido) | Bien |
| Muy bajo | Alto (**brecha grande**) | Sobreajuste |

### 2.4 Validación cruzada de 5 particiones (*5-fold cross-validation*)

No podemos medir el error con los mismos datos con los que el modelo aprendió: sería como calificar un examen con las respuestas a la vista. Por eso los 8,000 datos se reparten así:

```
Datos de entrenamiento (8,000 filas) → se dividen en 5 bloques de 1,600

Ronda 1:  [VALIDA] [entrena] [entrena] [entrena] [entrena]   → error 1
Ronda 2:  [entrena] [VALIDA] [entrena] [entrena] [entrena]   → error 2
Ronda 3:  [entrena] [entrena] [VALIDA] [entrena] [entrena]   → error 3
Ronda 4:  [entrena] [entrena] [entrena] [VALIDA] [entrena]   → error 4
Ronda 5:  [entrena] [entrena] [entrena] [entrena] [VALIDA]   → error 5

Resultado = promedio ± desviación estándar de los 5 errores
```

Cada fila se usa para validar **exactamente una vez**. El promedio estima cómo se comportará el modelo con datos nuevos y la desviación estándar indica qué tan estable es esa estimación.

### 2.5 Hiperparámetros y búsqueda en malla (*grid search*)

Los **hiperparámetros** son perillas que se fijan **antes** de entrenar y controlan qué tan flexible es el modelo (por ejemplo, el grado de un polinomio o la profundidad de un árbol). `GridSearchCV` prueba todas las combinaciones de una lista, evalúa cada una con validación cruzada y se queda con la de **menor error de validación**.

### 2.6 `Pipeline`: preparar los datos sin hacer trampa

Algunos modelos necesitan que las variables estén en la misma escala (**escalado**). Si escaláramos usando todos los datos antes de la validación cruzada, la información de los bloques de validación se «filtraría» al entrenamiento (**fuga de datos**). Un `Pipeline` encadena «escalar → modelo» y garantiza que en cada ronda el escalador aprenda **solo** de los datos de entrenamiento de esa ronda.

---

## 3. Mapa: instrucciones de la práctica → secciones del notebook

| Instrucción de la práctica | Puntos | Sección del notebook |
|---|---|---|
| Indicar al inicio las librerías y sus versiones | — | **0** |
| **1. EDA**: distribución de cada variable, correlaciones, faltantes y atípicos, documentar hallazgos | 20 (junto con preprocesamiento) | **1.1 – 1.5** |
| **2. Preprocesamiento**: separar predictores y objetivo, escalar cuando el método lo requiera, justificar | (incluido arriba) | **2** |
| **3. Modelos**: regresión lineal | 30 | **3.1** |
| Polinomial sin regularización (al menos dos grados) | | **3.2** (grados 2, 3 y 4) |
| Polinomial con regularización (Ridge/Lasso) con búsqueda del hiperparámetro | | **3.3** (Ridge, malla de grado × α) |
| SVR con kernel no lineal, ajustando C, epsilon y gamma | | **3.4** (RBF, 27 combinaciones) |
| Árbol de decisión, justificando la poda | | **3.5** (curva de profundidad + malla) |
| **Validación cruzada de 5 capas**: media y desviación de las métricas por modelo | 20 | **2** (protocolo) y **3.1 – 3.5** |
| **4. Tabla comparativa** y discusión del mejor modelo | 10 | **4** y **4.1** |
| **Evaluación final** en el conjunto de prueba: predicciones y RMSE de cada modelo | 20 | **5** |
| Conclusiones fundamentadas | (incluido en tabla) | **6** |
| Ejecutable de inicio a fin sin errores (Restart & Run All) | — | Todo el notebook |

---

## 4. Cómo ejecutar el notebook

### 4.1 Crear el entorno con `uv`

```bash
mkdir -p ~/maestria/examen-modulo2 && cd ~/maestria/examen-modulo2
uv init --bare
uv python pin 3.12
uv add "numpy==2.4.4" "pandas==3.0.2" "matplotlib==3.10.8" "scikit-learn==1.8.0" "scipy==1.17.1"
uv add --dev ipykernel
```

Copia a esa carpeta `Dzul_Christian_Examen_Modulo2.ipynb` y `electrical_grid_stability_train.csv`.

### 4.2 Ejecutar desde VS Code

1. Abre la carpeta con `code .` e instala las extensiones **Python** y **Jupyter**.
2. Abre el notebook y elige el kernel `.venv/bin/python` (**Select Kernel → Python Environments**).
3. Pulsa **Restart** y luego **Run All**.
4. La búsqueda del SVR (sección 3.4) es la parte más lenta: tarda alrededor de un minuto en un equipo con varios núcleos y más en uno con un solo núcleo.

> **Resultado esperado:** ninguna celda con error y, en la sección 5, el aviso de que no se encontró el archivo de prueba (es lo correcto si no lo tienes).

---

## 5. Recorrido sección por sección

### Sección 0 — Librerías y versiones

**Qué hace:** importa todo lo necesario y muestra una tabla con las versiones de Python y de cada librería.

| Librería | Para qué se usa en el notebook |
|---|---|
| `pandas` | Leer el CSV y manejar los datos en tablas (`DataFrame`) |
| `numpy` | Cálculos numéricos |
| `matplotlib` | Todas las gráficas |
| `scikit-learn` | Modelos, escalado, `Pipeline`, validación cruzada y métricas |
| `scipy` | Dependencia interna de scikit-learn |

**Por qué:** la práctica lo pide explícitamente, y además permite reproducir los resultados con las mismas versiones.

---

### Sección 1 — Análisis exploratorio de datos (EDA)

> **Instrucción:** *explorar la distribución de cada variable, revisar correlaciones, verificar faltantes o atípicos y documentar hallazgos.*

Antes de entrenar cualquier modelo hay que **conocer los datos**: qué valores toman, si hay errores y qué variables parecen relacionarse con `stab`.

#### 1.1 Carga y calidad de los datos
- Lee el CSV y muestra sus dimensiones: **8,000 filas × 13 columnas**.
- Cuenta valores faltantes (**0**) y filas duplicadas (**0**).
- `describe()` muestra para cada columna la media, la desviación estándar, el mínimo, los cuartiles y el máximo; se agregan la **asimetría** (si la distribución está «cargada» a un lado) y la **curtosis** (qué tan pesadas son sus colas).
- Se verifica el balance de potencia: la suma `p1 + p2 + p3 + p4` vale como máximo `1e-09`, es decir, **cero**. `p1` es exactamente `-(p2 + p3 + p4)`.
- Se calcula qué porcentaje de los casos es inestable: **63.6 %**.

#### 1.2 Distribución de cada variable
Histogramas de las 13 columnas. Casi todas tienen forma **plana (uniforme)**: los valores están repartidos parejo dentro de su rango, como corresponde a datos simulados. `p1` tiene forma de campana porque es la suma de tres variables.

#### 1.3 Valores atípicos (regla del IQR)
Un dato se considera atípico si cae lejos del 50 % central de los datos:

```
IQR = Q3 − Q1          (ancho del 50 % central)
atípico si  x < Q1 − k·IQR   o   x > Q3 + k·IQR      (k = 1.5 o k = 3)
```

Resultado: solo **1 valor** atípico (en `p1`, con k = 1.5) y **ninguno** con k = 3. Por eso **no se aplica ningún tratamiento** de atípicos. Los boxplots de las variables estandarizadas lo confirman visualmente.

#### 1.4 Correlaciones
- **Mapa de calor** de la matriz de correlación de Pearson: mide qué tan alineadas están dos variables, de −1 a 1.
- Correlación de cada predictor con `stab`, con **Pearson** (relación lineal) y **Spearman** (relación monótona, basada en el orden de los datos).
- Lista de pares de predictores con correlación mayor a 0.1: solo aparece `p1` con `p2`, `p3` y `p4` (≈ 0.58), consecuencia del balance de potencia.
- Diagramas de dispersión de `stab` contra algunos predictores.

#### 1.5 Hallazgos (celda de texto)
Resume lo anterior. La conclusión clave: `tau` y `g` tienen correlaciones moderadas con `stab` (0.28 a 0.31), `p` casi nula, y **ninguna variable por sí sola explica la estabilidad**. Eso anticipa que se necesitan modelos capaces de capturar **relaciones no lineales**.

---

### Sección 2 — Preprocesamiento

> **Instrucción:** *separar predictores de la variable objetivo, escalar cuando el método lo requiera y justificar las decisiones.*

| Decisión | Justificación |
|---|---|
| `X` = predictores, `y` = `stab` | Separar lo que el modelo usa de lo que debe predecir |
| **Quitar `p1`** | Es una combinación exacta de `p2`–`p4`: no aporta información nueva y causa **colinealidad perfecta**, que vuelve inestable la regresión lineal. Se usan **11 predictores** en los cinco modelos |
| No imputar ni tratar atípicos | No hay faltantes ni atípicos relevantes |
| `StandardScaler` dentro de un `Pipeline` | Necesario para polinomios, Ridge y SVR (ver tabla abajo). Al ir dentro del `Pipeline` no hay fuga de datos |
| El árbol **no** se escala | Solo compara cada variable con un umbral; la escala no le afecta |
| `KFold(5, shuffle=True, random_state=42)` | Las **mismas 5 particiones** para todos los modelos: comparación justa y resultados reproducibles |

**¿Qué hace `StandardScaler`?** Transforma cada variable para que tenga media 0 y desviación estándar 1:

```
z = (x − media) / desviación_estándar
```

| Modelo | ¿Necesita escalar? | Por qué |
|---|---|---|
| Regresión lineal | No (se incluye para comparar coeficientes) | Las predicciones no cambian |
| Polinomial | Sí | Elevar a potencias variables de escalas distintas las descompensa |
| Ridge | Sí | Penaliza el tamaño de los coeficientes, que depende de las unidades |
| SVR (RBF) | Sí | Mide distancias entre puntos |
| Árbol | No | Solo compara con umbrales |

**Funciones auxiliares definidas aquí:**

| Función | Qué hace |
|---|---|
| `evalua_cv(modelo)` | Corre la validación cruzada de 5 folds y devuelve media y desviación de RMSE, MAE y R², el RMSE de entrenamiento y el RMSE de cada fold |
| `desde_busqueda(busq)` | Extrae esas mismas métricas de la mejor combinación de un `GridSearchCV` (sin volver a entrenar) |
| `muestra(res)` | Imprime las métricas en una sola línea legible |

**Línea base:** `DummyRegressor` predice siempre el promedio de `stab`. Su RMSE (**0.03694**) es el punto de referencia: cualquier modelo útil debe superarlo.

---

### Sección 3 — Implementación y entrenamiento de modelos

> **Instrucción:** *implementar y ajustar cinco modelos.*

Cada modelo sigue el mismo patrón:

```
1. Definir el Pipeline (escalado + modelo).
2. Elegir hiperparámetros con validación cruzada (si los tiene).
3. Guardar sus métricas de validación cruzada en el diccionario `resultados`.
4. Reentrenar la mejor configuración con las 8,000 filas y guardarla en `finales`
   (ese es el modelo que se usará con el archivo de prueba).
5. Interpretar los resultados en una celda de texto.
```

#### 3.1 Regresión lineal

**Idea:** ajusta un plano (la versión con muchas variables de una recta):

```
stab_predicho = b + w1·tau1 + w2·tau2 + ... + w11·g4
```

**Código clave:** `Pipeline([StandardScaler(), LinearRegression()])`.

**Resultado:** RMSE = **0.02209**, R² = **0.642**. El error de entrenamiento y el de validación son casi iguales (0.02205 frente a 0.02209): no hay sobreajuste, pero hay **subajuste**, porque un plano no puede representar una relación curva. La gráfica de coeficientes muestra que `tau` y `g` pesan en positivo y `p` casi nada, igual que en el EDA.

#### 3.2 Regresión polinomial sin regularización

**Idea:** crear nuevas columnas con potencias y productos de las variables (por ejemplo `tau1²`, `tau1·g3`) y luego aplicar regresión lineal. Así el modelo puede curvarse.

**Código clave:** `Pipeline([StandardScaler(), PolynomialFeatures(grado), LinearRegression()])`, para los grados 2, 3 y 4.

| Grado | Columnas generadas | RMSE entrenamiento | RMSE validación | Brecha |
|---|---|---|---|---|
| 2 | 77 | 0.01215 | 0.01234 | 1.5 % |
| 3 | 363 | 0.00808 | 0.00872 | 8.0 % |
| **4** | 1,364 | 0.00590 | **0.00812** | 37.7 % |

**Elección:** grado 4, porque tiene el menor error de validación. La brecha creciente avisa que subir más el grado empezaría a sobreajustar.

#### 3.3 Regresión polinomial con regularización (Ridge)

**Idea:** igual que el polinomial, pero se agrega un **castigo** a los coeficientes grandes. El parámetro `α` (alpha) controla qué tan fuerte es el castigo: `α` chico ≈ sin castigo; `α` grande = modelo más rígido.

**Código clave:** `GridSearchCV` busca a la vez el grado (2, 3, 4) y `α` (0.001 a 1000): 21 combinaciones × 5 folds.

**Resultado:** mejor grado 4 con α = 1; RMSE = **0.00812**, **igual** que sin regularizar. Con α ≥ 100 el error sube.

**Por qué Ridge no mejoró:** hay muchas filas (6,400 por fold) para relativamente pocas columnas (1,364), así que el modelo no está en riesgo fuerte de sobreajuste. La regularización ayuda sobre todo cuando el número de variables se acerca al de observaciones.

#### 3.4 SVR (Support Vector Regression) con kernel RBF

**Idea:** SVR traza una función rodeada de un **«tubo»** de ancho ±ε. Los errores dentro del tubo no se castigan; solo los que se salen. Con el **kernel RBF**, la función puede curvarse de forma flexible.

| Hiperparámetro | Qué controla | Valores probados |
|---|---|---|
| `C` | Cuánto se castiga salirse del tubo (más alto = sigue más de cerca los datos) | 0.1, 0.3, 1 |
| `γ` (gamma) | Qué tan local es la influencia de cada punto (más alto = más «memorizador») | 0.03, 0.1, 0.3 |
| `ε` (epsilon) | Ancho del tubo de tolerancia | 0.001, 0.003, 0.006 |

> `ε` se probó en milésimas porque `stab` varía en milésimas (desviación ≈ 0.037). El valor por defecto (0.1) sería más ancho que casi todo el rango de `stab` y el modelo no aprendería nada.

**Resultado:** mejor combinación C = 0.1, γ = 0.1, ε = 0.001; RMSE = **0.00734**, R² = **0.961**, **el mejor de todos**. Con γ = 0.3 el error sube a ≈ 0.010 (sobreajuste). El modelo final usa 6,101 **vectores de soporte** (los puntos que definen la solución): es preciso, pero pesado.

#### 3.5 Árbol de decisión

**Idea:** hace preguntas del tipo «¿`tau1` ≤ 5.2?» y divide los datos en grupos cada vez más pequeños; la predicción es el **promedio de `stab`** del grupo final (la **hoja**).

**Cómo se controló el sobreajuste (poda):**

1. **Curva de validación de `max_depth`:** sin límite, el árbol memoriza (error de entrenamiento 0). El error de validación es mínimo alrededor de profundidad 10.
2. **Búsqueda conjunta** de `max_depth` (6 a sin límite) y `min_samples_leaf` (1 a 40): obligar a que cada hoja tenga varios datos evita hojas que memorizan un solo caso.

**Resultado:** `max_depth` = 15 y `min_samples_leaf` = 10; RMSE = **0.01836**, R² = **0.753**, con 624 hojas. Mejor que la regresión lineal, pero peor que polinomios y SVR: un árbol aproxima con «escalones» una relación que en realidad es suave.

---

### Sección 4 — Comparación de resultados

> **Instrucción:** *reunir las métricas en una tabla comparativa y discutir cuál modelo tuvo mejor desempeño.*

| Celda | Qué muestra |
|---|---|
| Tabla comparativa | Por modelo: RMSE, MAE y R² (media ± desviación), RMSE de entrenamiento, brecha y mejora frente a la línea base, ordenados del mejor al peor |
| RMSE por fold | El error de cada modelo en cada una de las 5 particiones |
| Gráficas de barras | RMSE y R² con barras de error |
| Residuos del mejor modelo | Predicho contra real, residuos contra predicción e histograma de residuos |
| 4.1 Discusión | Interpretación de los resultados |

**Cómo leer la tabla:** el modelo con menor RMSE de validación es el mejor. Para saber si la diferencia entre dos modelos es real, se compara con la desviación entre folds: el SVR supera al polinomial por 0.00078, unas cinco veces esa desviación, y gana en **los 5 folds**. La ventaja es consistente, no casualidad.

---

### Sección 5 — Evaluación final en el conjunto de prueba

> **Instrucción:** *dejar el notebook listo para leer el archivo de prueba, generar las predicciones de cada modelo y calcular e imprimir su RMSE.*

**Qué hace la celda, paso a paso:**

```
¿Existe electrical_grid_stability_test.csv en la carpeta?
├─ No  → imprime un aviso y termina sin error (caso del alumno).
└─ Sí  → 1. Lo lee y toma los mismos 11 predictores.
         2. Cada uno de los 5 modelos finales (ya reentrenados con las 8,000 filas) predice stab.
         3. Guarda las predicciones en predicciones_test.csv (una columna por modelo).
         4. ¿El archivo trae la columna stab?
            ├─ Sí → calcula e imprime RMSE, MAE y R² de cada modelo.
            └─ No → indica que el RMSE se calculará cuando haya etiquetas.
```

> **Importante:** el conjunto de prueba **no se usa en ninguna decisión** previa. Todos los hiperparámetros se eligieron con validación cruzada sobre el archivo de entrenamiento. Si el profesor entrega las etiquetas por separado, basta asignarlas a la variable `Y_TEST_EXTERNA`.

---

### Sección 6 — Conclusiones

Resume los hallazgos: modelo recomendado, alternativa eficiente, efecto de la regularización, limitaciones de los modelos simples, qué esperar en el conjunto de prueba y posibles mejoras.

---

## 6. Resumen de resultados

| Lugar | Modelo | RMSE (validación) | R² | Diagnóstico |
|---|---|---|---|---|
| 🥇 1 | **SVR RBF** (C = 0.1, γ = 0.1, ε = 0.001) | **0.00734 ± 0.00016** | **0.961** | Bajo sesgo; brecha moderada |
| 2 | Polinomial grado 4 + Ridge (α = 1) | 0.00812 ± 0.00015 | 0.952 | Bajo sesgo; brecha 38 % |
| 2 | Polinomial grado 4 (sin regularización) | 0.00812 ± 0.00015 | 0.952 | Igual que con Ridge |
| 4 | Árbol (max_depth = 15, min_samples_leaf = 10) | 0.01836 ± 0.00041 | 0.753 | Aproxima con escalones |
| 5 | Regresión lineal | 0.02209 ± 0.00047 | 0.642 | Subajuste |
| — | Línea base (promedio) | 0.03694 | 0.000 | Referencia |

**En una frase:** la estabilidad de la red depende de forma **no lineal** de las variables. Por eso los modelos flexibles (SVR y polinomios) reducen el error en ~80 % respecto a la línea base, mientras que la regresión lineal y el árbol se quedan cortos.

---

## 7. Preguntas frecuentes

**¿Por qué se eliminó `p1`?**
Porque `p1 = -(p2 + p3 + p4)` exactamente. Conservarla repetiría información y causaría colinealidad perfecta en los modelos lineales.

**¿Por qué la sección 5 muestra un aviso en lugar de resultados?**
Porque el archivo de prueba lo conserva el profesor. Cuando él lo coloque en la carpeta y ejecute el notebook, se generarán las predicciones y, si el archivo tiene `stab`, el RMSE de cada modelo.

**¿Por qué no hay «accuracy»?**
Porque es un problema de regresión (se predice un número). Se usan RMSE, MAE y R². Como dato complementario, el SVR acierta el **signo** de `stab` (estable o inestable) en el 97.2 % de los casos.

**¿El RMSE de validación es exacto?**
Es una buena estimación, aunque ligeramente optimista: es el de la *mejor* combinación entre varias probadas. Una validación cruzada anidada lo corregiría, pero las diferencias entre modelos son mucho mayores que ese sesgo.

**¿Los resultados cambian si lo ejecuto otra vez?**
No. Todo usa `random_state=42` y particiones fijas. Pueden variar decimales mínimos con otras versiones de las librerías.

---

## 8. Glosario

| Término | Definición |
|---|---|
| **Atípico** | Valor muy alejado del resto de los datos |
| **Brecha** | Diferencia entre el error de validación y el de entrenamiento; grande indica sobreajuste |
| **Colinealidad** | Dos o más predictores que contienen la misma información |
| **Fold / partición** | Cada uno de los bloques en que se dividen los datos en la validación cruzada |
| **Fuga de datos** | Usar información de los datos de validación o prueba durante el entrenamiento |
| **Hiperparámetro** | Ajuste del modelo que se elige antes de entrenar (grado, α, C, γ, ε, profundidad…) |
| **Kernel RBF** | Función que permite al SVR curvarse midiendo qué tan parecidos son dos puntos |
| **Línea base** | Modelo trivial (predecir siempre el promedio) que sirve de referencia |
| **`Pipeline`** | Cadena de pasos (escalar → modelo) que se entrena como una sola pieza y evita fugas |
| **Regularización** | Castigo a los coeficientes grandes para evitar que el modelo memorice |
| **Residuo** | Valor real menos valor predicho |
| **Sobreajuste / subajuste** | Modelo que memoriza el ruido / modelo demasiado simple |
| **Validación cruzada** | Entrenar y validar varias veces rotando el bloque de validación |
| **Vector de soporte** | Punto de entrenamiento que define la solución de un SVR |
