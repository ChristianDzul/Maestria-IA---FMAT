import chromadb

# Cliente persistente: guarda en la carpeta "chroma/"
client = chromadb.PersistentClient(path="chroma")

# Obtiene (o crea si no existe) la colección
collection = client.get_or_create_collection(name="Bank_BBVA")


def add_chunks(ids, embeddings, documents, metadatas):
    """Guarda una tanda de chunks (con sus vectores y metadatos) en Chroma."""
    # TODO 1: llama a collection.add(...) pasándole
    #   ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )
    


def query_chunks(query_embedding, top_k=3):
    """Dado el vector de una pregunta, regresa los top_k chunks más parecidos."""
    results = collection.query(
        query_embeddings=[query_embedding],   # ojo: lista, aunque sea una sola pregunta
        n_results=top_k,
    )
    
    return results


# if __name__ == "__main__":
#     from embed import embed_text
#     print(f"Elementos en la colección: {collection.count()}")
#     # 3 chunks de prueba
#     textos = [
#         "El banco aprueba préstamos a clientes.",
#         "La institución financiera otorga créditos.",
#         "Me gusta comer tacos los domingos.",
#     ]
#     vectores = [embed_text(t) for t in textos]
#     ids = ["c0", "c1", "c2"]
#     metadatas = [{"source": "prueba.txt"} for _ in textos]

#     #add_chunks(ids, vectores, textos, metadatas)

#     # Consulta: algo relacionado con banca
#     pregunta = "¿Cómo funcionan los créditos bancarios?"
#     q_vec = embed_text(pregunta)
#     resultados = query_chunks(q_vec, top_k=2)

#     print(resultados)