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


# if __name__ == "__main__":
#     import numpy as np 

#     def coseno(a, b):
#         a, b = np.array(a), np.array(b)
#         return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

#     v1 = embed_text("El banco aprueba préstamos a clientes.")
#     v2 = embed_text("La institución financiera otorga créditos.")
#     v3 = embed_text("Me gusta comer tacos los domingos.")

#     print(f"Longitud del vector: {len(v1)}")
#     print(f"Similitud (parecidas) v1-v2: {coseno(v1, v2):.4f}")
#     print(f"Similitud (ajena)     v1-v3: {coseno(v1, v3):.4f}")