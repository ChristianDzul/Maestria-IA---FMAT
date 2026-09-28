import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

GEN_MODEL = "gemini-3.6-flash"   
MIN_SCORE = 0.3                   # umbral de abstención


def build_prompt(question: str, citations: list[dict]) -> str:
    """Arma el prompt con los chunks numerados y las instrucciones."""
    contexto = ""
    for i, c in enumerate(citations, start=1):
        contexto += f"[{i}] ({c['source']}) {c['text']}\n\n"

    prompt = f"""Eres un asistente que responde SOLO con el contexto proporcionado.
Responde en español o ingles dependiendo del idioma de la pregunta. Cita las fuentes usando [n] donde n es el número del fragmento.
Si el contexto no contiene la respuesta, di exactamente: "No tengo evidencia suficiente en el corpus para responder."

Contexto:
{contexto}
Pregunta: {question}

Respuesta:"""
    return prompt


def _generar_con_reintentos(prompt: str, model: str, intentos: int = 3, espera: float = 2.5):
    """Llama a Gemini reintentando si el error es transitorio (503 / sobrecarga)."""
    ultimo_error = None
    for i in range(intentos):
        try:
            return client.models.generate_content(model=model, contents=prompt)
        except Exception as e:
            ultimo_error = e
            transitorio = any(
                s in str(e).lower()
                for s in ["503", "unavailable", "overloaded", "high demand"]
            )
            # Si es transitorio y aún quedan intentos, espera y reintenta.
            if transitorio and i < intentos - 1:
                time.sleep(espera * (i + 1))   # espera creciente: 2s, luego 4s
                continue
            raise   # error no transitorio, o ya se agotaron los intentos
    raise ultimo_error



def generate_answer(question: str, citations: list[dict], model: str = GEN_MODEL) -> dict:
    """Se genera una respuesta anclada, o se abstiene si no hay evidencia."""

    if not citations or citations[0]["score"] < MIN_SCORE:
        answer = "No tengo evidencia suficiente en el corpus para responder."
        return {"answer": answer, "abstained": True}
    else:
        # Si pasa el umbral, arma el prompt y llama a Gemini:
        prompt = build_prompt(question, citations)
        try:
            response = _generar_con_reintentos(prompt, model) #esto permite reintentar en caso de error transitorio (saturacion o alta demanda)
            answer = response.text
            return {"answer": answer, "abstained": False}
        except Exception as e:
            answer = f"Hubo un error al generar la respuesta. Intenta de nuevo en un momento. {e}"
            return {"answer": answer, "abstained": False, "error": str(e), }
