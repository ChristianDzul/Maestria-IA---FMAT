from fastapi import FastAPI

app = FastAPI(title="RAG Bancario")

@app.get("/health")
def health():
    # TODO: devuelve un diccionario simple,
    # por ejemplo {"status": "ok"}
    return {"status": "ok"}