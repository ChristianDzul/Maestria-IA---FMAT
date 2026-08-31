# 🎓 Maestria en Inteligencia Artificial

#### Fecha: `[27/08/2002]`

#### 📌 Notas y Hallazgos (Día 02):

> _Notas de clase:_

#### _Agents and environments_

Agents include humans, robots, softbots, thermostats, etc.
The agent executes actions and then perceives it.

![alt text](image-2.png)

The agent function maps from percept histories to actions:

![alt text](image-3.png)

The agent program runs on the physical architecture to produce "f".

- Example of Vacuum-cleaner:

Percepts: location and contents (pos A, state: Dirty)
Actions: move to the left, right, Suck, NoOperation.

- Posibilities:

![alt text](image-5.png)

- Rationality:

A system/agent is rational when:

![alt text](image-6.png)

- Peas

To desing a rational agent, we must specify the task environment. Consider, eg, the task of designing an automated taxi:

- Performance measure
- Environment: Objetos con los que interactuara.
- Actuators: Aquello que te permite ejecutar las acciones en tu ambiente.
- Sensors: Como el agente percibira el ambiente, que esta pasando en el.

![alt text](image-7.png)

Otro ejemplo:
![alt text](image-8.png)

En cuanto el ambiente, hay que considerar las siguientes caracteristicas o tipos:

Sea observable: Tal cual se pueda observar con detalle.
Deterministico: Que ya se sabe que ocurrira con cierta accion, no tiene aletoriedad. no son estocastivo.
Episodico: Sistemas donde puede funcionar en diferentes acciones, que sea versatil, que no sea secuencial.
Estatico: Es que no hay variabilidad en el ambiente donde se esta desarrollando.
Discreto: conjunto finito de estados y acciones/numeros
Single-agent: el uso de un solo agente (no multiagente)

![alt text](image-9.png)

#### _Agemt types_

There are many, but the basic types are:

- Simple reflex agents:

No tiene memoria, puede ser mas para consultas.

![alt text](image-10.png)

- Reflex agents with state:

Lleva registro de lo que va persibiendo, guardndo contexto y memoria.

![alt text](image-11.png)

- Goal-based agents:

Contiene todo lo anterior, pero adicionalmente, puede saber que es una meta. Ademas de llevar registro, este mismo se puede establecer metas que maximisen su desempeño.

![alt text](image-17.png)

- Utility-based agents

Este optimiza seleccionando la opcion que mejor le conviene tanto en tiempo, como en performance, ajustado a la necesidad.

![alt text](image-12.png)

- Learning agents

Aquellos que tienen una arquitectura que aprende por refuerzo y recompensas. Que le permite a identificar cuando hacer o no una accion o respuesta dado a los refuerzos con los que ha aprendido. Reinforcement learning. Es el modelo de agente mas moderno y utilizada.

![alt text](image-13.png)

#### _Rational agents_

An agents is an entity that perceives and acts. This clase is about designing rational agents.

> _Notas generales:_

- Las grabaciones se guardaran en teams oficial de la UADY.
- La proxima semana ya nos daran nuestras credenciales para el correo constitucional.
- Las tareas se guardan con la nomenglatura:
  ![alt text](image.png)
- Contestar el formulario para compartir mi URL/Profile de github.
- Para las tareas de esta semana sera el 04 de septiembre del 2026:
  ![alt text](image-1.png)
- AlumnoFMAT9 (para acceso en computadora)
- Alan Turing "Father of AI"
- Agentes >> ejercicios >> ejercicio 01 >> El mundo de wumpus

clonar lo de wumpus, ejecutar cada programa de wumpus, leer el README.md para la creacion del entorno e instalar paqueterias necesarias y asi poder ejecutar los scripts de Python.

![alt text](image-15.png)

![alt text](image-16.png)

---

#### Fecha: `[28/08/2002]`

#### 📌 Notas y Hallazgos (Día 03):

#### Metodos de busqueda

- Tree search

Va buscando branch por branch, estado, o nodo hasta llegar al objetivo.
![alt text](image-18.png)

> _Notas generales:_

- reubicar wumpus, agujeros, etc. El tamanio del agente. Y modificar esto en el yaml, posteriormente correrlo los agentes
