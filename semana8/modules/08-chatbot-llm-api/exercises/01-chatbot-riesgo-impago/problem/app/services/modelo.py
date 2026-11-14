import joblib

from app.config import MODEL_PATH
from app.schemas.prestamo import PrediccionSalida, PrestamoEntrada

# Conservo el orden de entrenamiento indicado en el enunciado.
VARIABLES = [
    "edad",
    "ingresos_mensuales",
    "importe_prestamo",
    "plazo_meses",
    "antiguedad_laboral_anios",
    "impagos_previos",
]

# Cargo el artefacto de clase una vez por proceso, al importar el módulo.
modelo = joblib.load(MODEL_PATH)


def decidir(probabilidad: float) -> str:
    if probabilidad < 0.2:
        return "aprobar"
    if probabilidad < 0.5:
        return "revisar"
    return "rechazar"


def predecir(entrada: PrestamoEntrada) -> PrediccionSalida:
    valores = [getattr(entrada, variable) for variable in VARIABLES]
    # La columna 1 corresponde al impago en el modelo docente.
    probabilidad = float(modelo.predict_proba([valores])[0][1])
    return PrediccionSalida(
        probabilidad_impago=probabilidad, decision=decidir(probabilidad)
    )
