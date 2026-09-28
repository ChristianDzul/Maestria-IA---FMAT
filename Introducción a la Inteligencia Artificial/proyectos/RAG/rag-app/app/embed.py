from google import genai
import os
from dotenv import load_dotenv


load_dotenv()  # Carga las variables de entorno desde el archivo .env
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def embed_text(text: str) -> list[float]:
    """
    Genera un embedding para el texto dado usando el modelo "gemini-embedding-001".
    """
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )
    return result.embeddings[0].values
