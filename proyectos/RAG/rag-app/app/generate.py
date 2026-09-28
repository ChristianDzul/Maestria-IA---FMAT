import os
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


def generate_answer(question: str, citations: list[dict], model: str = GEN_MODEL) -> dict:
    """Se genera una respuesta anclada, o se abstiene si no hay evidencia."""

    if not citations or citations[0]["score"] < MIN_SCORE:
        answer = "No tengo evidencia suficiente en el corpus para responder."
        return {"answer": answer, "abstained": True}
    else:
        # Si pasa el umbral, arma el prompt y llama a Gemini:
        prompt = build_prompt(question, citations)
        try:
            response = client.models.generate_content(model=model, contents=prompt)
            answer = response.text
            return {"answer": answer, "abstained": False}
        except Exception as e:
            answer = f"Hubo un error al generar la respuesta. Intenta de nuevo en un momento. {e}"
            return {"answer": answer, "abstained": False, "error": str(e), }
