from fastapi import APIRouter, Depends

from app.schemas.chat import ChatEntrada, ChatSalida
from app.services.llm import get_llm
from app.services.orquestador import responder

router = APIRouter()


@router.post("/chat", response_model=ChatSalida)
def chat(entrada: ChatEntrada, llm=Depends(get_llm)) -> ChatSalida:
    # La dependencia permite sustituir el cliente en tests sin usar la red.
    return responder(entrada.mensajes, llm)
