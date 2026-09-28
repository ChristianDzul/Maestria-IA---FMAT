import chromadb
from pathlib import Path

# store.py está en rag-app/app/ → subimos a rag-app/ y apuntamos a chroma/
CHROMA_DIR = Path(__file__).resolve().parent.parent / "chroma"

# Guarda en la carpeta "chroma/"
client = chromadb.PersistentClient(path=str(CHROMA_DIR))

# Obtiene (o crea si no existe) la colección
collection = client.get_or_create_collection(name="Bank_BBVA")


def add_chunks(ids, embeddings, documents, metadatas):
    """Guarda una tanda de chunks (con sus vectores y metadatos) en Chroma."""
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )
    


def query_chunks(query_embedding, top_k=3):
    """Dado el vector de una pregunta, regresa los top_k chunks más parecidos."""
    results = collection.query(
        query_embeddings=[query_embedding],   # En modo lista, aunque sea una sola pregunta
        n_results=top_k,
    )
    
    return results