import json

from pydantic import ValidationError

from app.schemas.chat import ChatSalida, HerramientaUsada
from app.schemas.prestamo import PrestamoEntrada
from app.services.modelo import predecir

NOMBRE_TOOL = "calcular_riesgo_impago"
MAX_VUELTAS = 4

SISTEMA = (
    "Eres un asistente de riesgo de un banco. Cuando tengas todos los datos de una solicitud de "
    "prestamo, llama a la herramienta calcular_riesgo_impago. Si falta algun dato, pidelo. "
    "Nunca inventes valores. Responde en espanol y de forma breve."
)


def leer_argumentos(texto):
    """YA HECHO: convierte el texto JSON de la tool en dict ({} si no es JSON valido)."""
    try:
        datos = json.loads(texto)
    except (json.JSONDecodeError, TypeError):
        return {}
    if isinstance(datos, dict):
        return datos
    return {}


def definir_tool() -> dict:
    # Uso el mismo contrato para informar al LLM y para validar su llamada.
    return {
        "type": "function",
        "function": {
            "name": NOMBRE_TOOL,
            "description": "Calcula el riesgo de impago con los seis datos de la solicitud.",
            "parameters": PrestamoEntrada.model_json_schema(),
        },
    }


def ejecutar_tool(nombre, argumentos_json) -> dict:
    if nombre != NOMBRE_TOOL:
        return {"ok": False, "error": "Herramienta desconocida."}
    try:
        entrada = PrestamoEntrada.model_validate_json(argumentos_json)
        salida = predecir(entrada)
        return {"ok": True, **salida.model_dump()}
    except ValidationError as error:
        # Devuelvo el detalle de validación para que el LLM pueda corregirse.
        return {"ok": False, "error": str(error)}
    except Exception:
        # Esta frontera devuelve ok incluso si falla la inferencia.
        return {"ok": False, "error": "No se ha podido ejecutar el cálculo de riesgo."}


def responder(mensajes, llm) -> ChatSalida:
    # Trabajo sobre una lista nueva para no modificar el historial del frontend.
    historial = [{"role": "system", "content": SISTEMA}]
    historial.extend(mensaje.model_dump() for mensaje in mensajes)
    herramientas = [definir_tool()]
    ultima_herramienta = None

    for _ in range(MAX_VUELTAS):
        mensaje = llm.completar(historial, herramientas)
        llamadas = mensaje.get("tool_calls") or []
        if not llamadas:
            return ChatSalida(
                respuesta=mensaje.get("content") or "No he recibido una respuesta de texto.",
                herramienta=ultima_herramienta,
            )

        # Conservo la petición del asistente y relaciono cada resultado con su id.
        historial.append(mensaje)
        for llamada in llamadas:
            funcion = llamada["function"]
            resultado = ejecutar_tool(funcion["name"], funcion["arguments"])
            historial.append({
                "role": "tool",
                "tool_call_id": llamada["id"],
                "name": funcion["name"],
                "content": json.dumps(resultado, ensure_ascii=False),
            })
            ultima_herramienta = HerramientaUsada(
                nombre=funcion["name"],
                argumentos=leer_argumentos(funcion["arguments"]),
                resultado=resultado,
            )

    # El límite cuenta llamadas al LLM; no hago una quinta para redactar el cierre.
    return ChatSalida(
        respuesta="He alcanzado el límite de intentos. Revisa los datos de la solicitud.",
        herramienta=ultima_herramienta,
    )
