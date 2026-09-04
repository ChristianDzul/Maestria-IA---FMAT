# Ejercicio 03 — Descripción PEAS de agentes inteligentes

**Materia:** Introducción a la Inteligencia Artificial
**Unidad / Módulo:** Agentes
**Actividad:** Actividad
**Estudiante:** Christian Isaac Dzul Canul
**Programa:** Maestría en Inteligencia Artificial 🎓
**Docente:** Dr. Víctor Uc Cetina
**Fecha:** `03/09/2026`

---
> ## 1. Objetivo

Para cada una de las 8 aplicaciones listadas abajo, redacta una descripción PEAS completa y coherente. Debes pensar como diseñador del agente: qué optimiza, dónde actúa, con qué puede mover o modificar el mundo, y qué puede observar.

---

> ## 2. Desarollo

### `1. Asistente virtual de voz (p. ej. Siri, Alexa o Google Assistant en un altavoz inteligente).`

   - **Performance:** Calidad de respuesta (sea correcta y precisa), provea la informacion en el menor tiempo posible, comandos o solicitudes ejecutados correctamente (reproducir música, llamar a algun contacto, enviar mensaje, etc), nivel de satisfacción del usuario, nivel de seguridad.

   - **Environment:** En el hogar o sitio, los usuarios, conectividad a internet o con otros agentes. Adicionalmente, en cuanto al tipo de entorno, este es:
   
      - Parcialmente observable ya que no tiene acceso completo a dispositivos sino a ciertas caracteristicas. 
      - Secuencial ya que el agente de voz puede retener informacion previamente solicitada, por ejemplo solcitar que Alexa reproduzca nuevamente una canción.
      - Estocastico ya que las respuestas como informacion solicitada al agente de paginas web pueden ser diferentes.
      - Dinamico dado que el entorno en donde se desarolla puede variar, ya sea por ejemplo que el usuario cancele la accion del asistente virtual, llegue una notificacion en el dispositivo, que cambie el estado de una accion que iba a realizar como por ejemplo el apagar una foco.

   - **Actuators:** Acceso a información local y atravez de páginas web, lectura de contactos y contestar/hacer llamadas telefonicas, acceso a aplicaciones de terceros como Spotify o sistema de navegacion (google maps), mensajeria. 

   - **Sensors:** microfono para detectar comando por voz, acceso a internet y uso de APIs, sensor o boton manual para ejecutar comando de voz, acceso a dispositivos como lamparas, tvs, consolas, entre otros que esten accesibles para el agente de voz.

### `2. Robot aspirador doméstico (p. ej. Roomba u otro robot que limpia pisos de un departamento).`

   - **Performance:** Área total limpiada, eficiencia para no repetir zonas ya limpiadas, detección y recolección de suciedad, cantidad total de errores (caídas por escaleras, estancamientos, y choques con obstáculos), tiempo de limpieza, duración de uso de la batería, regreso exitoso a la base de carga.

   - **Environment:** El hogar/departamento, pisos de distintos materiales (alfombra, madera, cerámica), muebles, mascotas y personas que se mueven por el espacio, objetos u obstáculos. En cuanto al tipo de entorno, este es:

      - Parcialmente observable ya que el robot solo percibe su entorno inmediato a través de sus sensores, no tiene un mapa completo desde el inicio.
      - Secuencial ya que las decisiones de movimiento actuales afectan las zonas que quedan por limpiar y las rutas futuras.
      - Estocástico ya que no siempre puede predecir con certeza la posición de obstáculos como mascotas o personas.
      - Dinámico dado que el entorno puede cambiar mientras el robot limpia, por ejemplo que alguien mueva una silla o el robot deba esquivar a una mascota que se cruza.

   - **Actuators:** Motores de las ruedas para movimiento, succión y cepillos para recolectar suciedad, base de carga.

   - **Sensors:** Sensores de choque y/ proximidad, sensores infrarrojos o láserpara mapeo y detección de obstáculos, gestor de batería, sensor y/o cámara para detectar zonas más sucias. 

### `3. Sistema de recomendación de streaming (p. ej. Netflix o Spotify que sugiere películas o canciones).`

   - **Performance:** Relevancia y precisión de las recomendaciones respecto a los gustos del usuario, tasa de interacción (clics, reproducciones completas), retención y tiempo de uso de la plataforma, variedad en el contenido sugerido, satisfacción del usuario. 

   - **Environment:** La plataforma en uso (youtube, tidal, spotify, Netlfix, etc), el catálogo de contenido disponible (generos musicales y/o tipo de videos, series, peliculas, etc), el historial y comportamiento del usuario. En cuanto al tipo de entorno, este es:

      - Parcialmente observable ya que el sistema no conoce con certeza las preferencias reales del usuario, solo infiere a partir de su comportamiento observado/recabado.
      - Secuencial ya que las recomendaciones e interacciones pasadas del usuario influyen en las recomendaciones futuras.
      - Estocástico ya que la reacción del usuario ante una recomendación no es completamente predecible, pueden haber errores.
      - Dinámico dado que el catálogo de contenido cambia constantemente y los gustos del usuario también pueden evolucionar con el tiempo.

   - **Actuators:** Presentación de listas de contenido recomendado, notificaciones en el dispositivo o por correo, ajuste del orden de la interfaz según el perfil del usuario, generación de playlists automáticas.

   - **Sensors:** Registro de clics, reproducciones, tiempo de visualización o escucha, calificaciones o "me gusta", historial de búsquedas, datos de perfil del usuario, patrones de otros usuarios similares.

### `4. Vehículo autónomo en ciudad (conducción sin conductor en calles urbanas con tráfico y peatones).`

   - **Performance:** Seguridad (evitar accidentes y choques), cumplimiento de normas de tránsito, tiempo de llegada al destino, comodidad del usuario en la conducción (aceleración y frenado suaves), eficiencia en el consumo de combustible o batería, correcta interpretación de señales y semáforos.

   - **Environment:** Calles urbanas, tráfico, peatones, ciclistas, semáforos y señalización, condiciones climáticas. En cuanto al tipo de entorno, este es:

      - Parcialmente observable ya que el vehículo no puede ver más allá del alcance de sus sensores ni predecir con certeza las intenciones de otros conductores o peatones.
      - Secuencial ya que las decisiones de conducción actuales (como cambiar de carril) afectan las opciones y riesgos en los siguientes momentos del trayecto.
      - Estocástico ya que el comportamiento de otros conductores, peatones y las condiciones del tráfico no son completamente predecibles.
      - Dinámico dado que el entorno cambia constantemente dado por otros autos moviéndose, peatones cruzando o cambios repentinos en el tráfico.

   - **Actuators:** Volante, acelerador, frenos, luces direccionales, bocina, pantalla para visualizar la ruta.

   - **Sensors:** Cámaras, sensor tipo LIDAR para mapeo, sensores de proximidad, GPS, sensores de velocidad de las ruedas.

### `5. Agente de trading algorítmico en bolsa (compra y venta automática de acciones en mercados financieros).`

   - **Performance:** Rentabilidad, minimización de riesgo (control de pérdidas), velocidad de ejecución de las órdenes, precisión en la predicción con respecto a las tendencias del mercado.

   - **Environment:** Los mercado financieros, otros agentes de trading, noticias y eventos económicos globales, plataformas de intercambio de valores. En cuanto al tipo de entorno, este es:

      - Parcialmente observable ya que el agente no tiene acceso a toda la información relevante del mercado (por ejemplo, intenciones de otros traders o eventos futuros).
      - Secuencial ya que las decisiones de compra o venta pasadas afectan la posición financiera y las decisiones futuras del agente.
      - Estocástico ya que los movimientos del mercado dependen de múltiples factores impredecibles.
      - Dinámico dado que los precios y condiciones del mercado cambian constantemente.

   - **Actuators:** Envío de órdenes de compra/venta a la plataforma de trading, ajuste de portafolio, cancelación o modificación de órdenes pendientes.

   - **Sensors:** Acceso a datos de precios en tiempo real, indicadores técnicos y financieros, volumen de transacciones, datos históricos del mercado.

### `6. Sistema de diagnóstico médico asistido por IA (apoya a un médico a interpretar síntomas e imágenes clínicas).`

   - **Performance:** Precisión del diagnóstico, tiempo de respuesta, claridad de la explicación, cumplimiento de estándares clínicos, capacidad de sugerir diagnósticos que puedan ser falsos positivos.

   - **Environment:** Hospitales, clinicas, historiales médicos de pacientes, imágenes o resultados de pruebas (rayos X, resonancias, etc.), el médico como usuario que valida o descarta la sugerencia. En cuanto al tipo de entorno, este es:

      - Parcialmente observable ya que el sistema no deberia tener acceso a toda la información clínica del paciente, solo a los datos e imágenes que se le proporcionan.
      - Secuencial ya que un diagnóstico o recomendación puede influir en estudios o decisiones médicas posteriores para el mismo paciente.
      - Estocástico ya que la relación entre síntomas/imágenes y la condición real del paciente pueden variar por varios factores.
      - Dinámico dado que el estado de salud del paciente puede cambiar entre una consulta y otra, o incluso llegar nueva información durante el análisis.

   - **Actuators:** Generación de reportes o sugerencias de diagnóstico, resaltado de áreas relevantes, recomendaciones de estudios adicionales.

   - **Sensors:** Entrada de datos clínicos (síntomas, historial), imágenes médicas, resultados de laboratorio.

### `7. Dron de inspección de infraestructura (revisa grietas, corrosión o fugas en puentes, tuberías o líneas eléctricas).`

   - **Performance:** Precisión en la detección de daños (grietas, corrosión, fugas), cobertura completa de la estructura inspeccionada, tiempo de inspección, seguridad del vuelo (evitar colisiones), calidad de las imágenes o datos capturados.

   - **Environment:** Estructuras de infraestructura (puentes, edificios, instalaciones eléctricas), condiciones climáticas (viento, lluvia), obstáculos físicos cercanos a la estructura, espacio aéreo. En cuanto al tipo de entorno, este es:

      - Parcialmente observable ya que el dron solo percibe el área cubierta por sus sensores y cámaras en cada momento del vuelo.
      - Secuencial ya que la ruta de inspección recorrida previamente determina qué zonas faltan por revisar.
      - Estocástico ya que factores como ráfagas de viento o interferencias pueden afectar el vuelo de forma impredecible.
      - Dinámico dado que las condiciones climáticas y el entorno alrededor de la estructura pueden cambiar durante la inspección.

   - **Actuators:** Motores y hélices para el vuelo, cámaras para deteccion y captura de las zonas afectadas, luces para inspección en zonas oscuras.

   - **Sensors:** Cámaras de alta resolución, sensores de mapeo, GPS, sensores de proximidad/obstáculos, sensores de viento y altitud.

### `8. Agente jugador de ajedrez (programa que compite contra un humano u otro agente en partidas completas).`

   - **Performance:** Porcentaje de partidas ganadas, calidad de las jugadas, tiempo de respuesta por jugada, cumplimiento de las reglas del juego, capacidad de predecir jugadas del oponente.

   - **Environment:** El tablero de ajedrez, las piezas y su posición, el oponente, el reloj de juego (si aplica, usualmente en competencias mas serias). En cuanto al tipo de entorno, este es:

      - Totalmente observable ya que el agente tiene acceso completo al estado del tablero en todo momento.
      - Secuencial ya que cada jugada realizada afecta directamente las opciones y el desarrollo de las jugadas siguientes.
      - Determinístico ya que el resultado de cada movimiento está completamente definido por las reglas del juego, sin factores de azar.
      - Estático o semi dinámico si se juega con reloj, ya que el tablero no cambia mientras el agente decide su jugada, aunque el tiempo disponible puede ir reduciéndose.

   - **Actuators:** Movimiento de piezas en el tablero, notificación de jugada al oponente, pulsar el reloj tras cada jugada.

   - **Sensors:** Lectura del estado actual del tablero, reconocimiento de la jugada realizada por el oponente, cámaras o sensores de posición de piezas.

---
> ## 4. Criteria

1. No usar IA para generar las respuestas de este ejercicio.
2. Hay exactamente 8 descripciones PEAS, una por cada aplicación de la lista.
3. Cada descripción tiene los cuatro componentes (P, E, A, S) claramente identificados.
4. Las respuestas son específicas de la aplicación (evita copiar la misma descripción genérica para todas).
5. El entorno (E) incluye al menos una clasificación AIMA (p. ej. parcialmente observable, estocástico, secuencial).
6. Redacción clara, en español, sin ambigüedades evidentes.