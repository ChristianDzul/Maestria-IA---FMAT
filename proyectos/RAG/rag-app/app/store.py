import chromadb

# Guarda en la carpeta "chroma/"
client = chromadb.PersistentClient(path="chroma")

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