# app/chunk.py

def chunk_text(text: str, chunk_size: int = 300, overlap: int = 60) -> list[str]:
    """
    Divide `text` en fragmentos de `chunk_size` palabras,
    solapando `overlap` palabras entre fragmento y fragmento.
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        #Obtén el sub-fragmento de palabras desde `start` hasta `end`
        word_chunk = " ".join(words[start:end])
        # Agrega ese string a la lista `chunks`
        chunks.append(word_chunk)
        #Update `start` para el siguiente fragmento, teniendo en cuenta el solapamiento
        start = end - overlap
        if start >= len(words):
            break
        pass

    return chunks


# if __name__ == "__main__":
#     with open("data/03_command_center_operacion_y_matriz_raci.md", "r", encoding="utf-8") as f:
#         texto = f.read()

#     resultado = chunk_text(texto, chunk_size=300, overlap=60)

#     print(f"Total de palabras en el texto: {len(texto.split())}")
#     print(f"Total de chunks: {len(resultado)}")
#     for i, chunk in enumerate(resultado):
#         print(f"\n--- Chunk {i + 1} ---")
#         print(chunk)
        
    # print("\n--- Primer chunk ---")
    # print(resultado[0])
    # print("\n--- Segundo chunk ---")
    # print(resultado[1])