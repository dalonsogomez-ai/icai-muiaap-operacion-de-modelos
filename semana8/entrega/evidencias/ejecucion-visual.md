# Ejecución visual — 14/11/2026

Interacción real con Ordenador en Visual Studio Code, worktree icai-semana8-tareas.
La salida de comandos está en los ficheros de evidencia, no reconstruida a mano.

- Terminal integrada: creación del worktree, copia del starter, uv sync, implementación de los cinco archivos y uv run pytest.
- Regeneración del modelo con el script docente y repetición de los 31 tests: todos pasan.
- Uvicorn: API local 127.0.0.1:8000. Streamlit: 127.0.0.1:8501, abierto en el navegador integrado del editor.
- Primer ejemplo completo: respuesta de 16.4 % y aprobar. Desplegado el panel de la tool: seis argumentos correctos y resultado coincidente.
- Nueva conversación: edad 30 e ingresos 2500. La respuesta pide importe, plazo, antigüedad e impagos; no muestra una tool.
- Segundo turno: importe 12000, plazo 36, antigüedad 5 e impagos 0. La conversación conserva los datos anteriores y devuelve 16.4 % y aprobar.
- Nueva conversación: edad 20 y antigüedad 15, con el resto de datos completo. El chat devuelve el error del validator sin caída del servidor.

El assignment pide probar el chatbot completo y la suite en verde; no impone capturas.
