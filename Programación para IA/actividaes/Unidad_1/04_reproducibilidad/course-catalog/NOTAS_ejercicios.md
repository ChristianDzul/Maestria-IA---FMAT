# Borrador de respuestas (Unidad 1 · Sesión 4)

---
## Ejercicio 1 · Punto de entrada (versión final para README)
1. import main no consulta: importar solo define; main() corre bajo
   `if __name__ == "__main__"`. Al importar, __name__ == "main" (no "__main__").
2. En server.py, ese mismo guard envuelve `mcp.run(transport="stdio")`, así que
   importar server no inicia el transporte (al importar, __name__ == "server").
3. Registrar (decorador @mcp.tool() al importar, engancha find_courses) vs
   iniciar (mcp.run(stdio) bajo __main__, abre el transporte y espera).
   Por eso pruebas y cliente pueden importar server sin arrancar el servidor.

## Ejercicio 2 · Datos y argumentos
- data/extra_courses.json = copia de courses.json + PY03 "Python for machine learning".
- `main.py python --catalog data/extra_courses.json` -> 3 resultados (PY01, PY02, PY03).
- Ruta inexistente -> FileNotFoundError (OSError) -> ERROR + traceback, código 1.
  No es "sin coincidencias" (eso sería lista vacía, código 0).
- find_courses (MCP) usa search_courses(query) con el catálogo por defecto, así que
  `client.py python` sigue dando 2 (PY01, PY02). --catalog es solo de main.py.

## Ejercicio 3 · Niveles y destinos
- DEBUG: consola muestra DEBUG (ruta del catálogo) + INFO (coincidencias).
- INFO: consola muestra solo INFO.
- ERROR: consola no muestra INFO/DEBUG (consulta exitosa, sin error); solo JSON.
- --log-level ERROR --log-file logs/app.log: consola solo JSON; el archivo guarda
  DEBUG e INFO.
- Por qué: el logger raíz acepta desde DEBUG; el handler de CONSOLA filtra por
  --log-level, pero el handler de ARCHIVO está fijo en DEBUG -> el archivo
  conserva lo que la consola oculta.
- stdout en server.py: el protocolo MCP (stdio) usa stdout para sus mensajes JSON;
  un print/log en stdout lo corrompería. Por eso logs -> stderr, diagnóstico en stderr.

## Ejercicio 4 · Mejorar el diagnóstico
- En catalog/search.py, la línea INFO ahora es:
  logger.info("Search completed: %d matches out of %d courses", len(matches), len(courses))
- Usa argumentos de logging (%d + valores), no f-string: el texto se forma solo si
  INFO está activo.
- Resultados sin cambios: main.py python -> PY01, PY02 (2); client.py python -> PY01, PY02 (2).
  Solo cambió el texto del log ("2 matches out of 3 courses").
- Como el módulo lo usan main.py y la herramienta MCP, el mejor diagnóstico aplica a ambos.

## Ejercicio 6 (calidad) · Horas negativas
- Course exige hours > 0 (Field(gt=0)). test_negative_hours escribe un catálogo
  temporal con hours: -5 y verifica pytest.raises(ValueError) en search_courses.
- ValidationError de Pydantic v2 hereda de ValueError (por eso se captura como ValueError).
- Datos inválidos -> error explícito, distinto de "sin coincidencias" (lista vacía).
- pytest pasa de 6 a 7 pruebas en verde.

## Ejercicio 7 (calidad) · Prueba de consola
- tests/test_console.py: subprocess.run ejecuta main.py con --catalog a un archivo
  inexistente (en tmp_path). Verifica returncode == 1 y stdout == "".
- Valida el contrato de la CLI end-to-end: error -> código 1 y stdout limpio
  (los errores van a stderr).
- pytest pasa de 7 a 8 pruebas en verde.

## Ejercicio 8 (calidad) · Import sin usar
- Agregado `import os` en main.py -> `ruff check .` falla con F401
  ("os imported but unused"), código != 0. (evidencia en ~/evidencia_ej8_ruff.txt)
- Corregido con `ruff check --fix` (o borrando la línea) -> "All checks passed!".
- Muestra que Ruff detecta/elimina imports muertos automáticamente. pytest sigue en 8.
