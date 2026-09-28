from fastapi import FastAPI
from pydantic import BaseModel

#imports relativos a RAG
from .chunk import chunk_text
from .embed import embed_text
from .store import add_chunks, query_chunks, collection   # importamos collection para contar
from .generate import generate_answer

app = FastAPI(title="RAG Bancario BBVA", description="API para RAG con FastAPI, Chroma y Gemini", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


# --- Modelo del cuerpo de /ingest ---
class IngestRequest(BaseModel):
    text: str
    source: str      


@app.post("/ingest")
def ingest(req: IngestRequest):
    # 1. Trocear el texto
    chunks = chunk_text(req.text, chunk_size=300, overlap=60)
    vectores = [embed_text(c) for c in chunks]

    #Los `ids` únicos por chunk.
    ids = [f"{req.source}_{i}" for i in range(len(chunks))]

    #los `metadatas`, un dict por chunk con al menos "source"
    metadatas = [{"source": req.source, "chunk_index": i} for i in range(len(chunks))]

    # 4. Guardar en Chroma
    add_chunks(ids=ids, embeddings=vectores, documents=chunks, metadatas=metadatas)
    

    # 5. Responder cuántos chunks se indexaron y cuántos hay en total en la colección
    return {
        "source": req.source,
        "chunks_indexed": len(chunks),
        "total_in_collection": collection.count(),
    }
    
# --- Modelo del cuerpo de /query ---
class QueryRequest(BaseModel):
    question: str
    top_k: int = 3
    model: str = "gemini-3.6-flash"       


@app.post("/query")
def query(req: QueryRequest):
    
    # 1. Incrustar la pregunta
    q_vec = embed_text(req.question)
    # 2. Consultar Chroma
    results = query_chunks(q_vec, top_k=req.top_k)
    # 3. Desenvolver la respuesta de Chroma y armar las citas
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    ids = results["ids"][0]

    #Lista `citations`, un dict por chunk recuperado.
    citations = []
    for i in range(len(documents)):
        citation = {
            "id": ids[i],
            "source": metadatas[i]["source"],
            "text": documents[i],
            "score": 1 - distances[i]
        }
        citations.append(citation)
    

    # Respuesta generada por Gemini, o abstención si no hay evidencia suficiente
    result = generate_answer(req.question, citations, model=req.model)

    return {
        "answer": result["answer"],       # utiliza la respuesta generada por generate_answer
        "citations": citations,
        "abstained": result["abstained"], # utiliza el valor de abstained de generate_answer
        "error": result.get("error", ""), #None si no hay error, o el mensaje de error si lo hay
    }    