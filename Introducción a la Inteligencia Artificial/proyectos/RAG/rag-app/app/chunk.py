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
        #sub-fragmento de palabras desde `start` hasta `end`
        word_chunk = " ".join(words[start:end])
        # Agrega ese string a la lista `chunks`
        chunks.append(word_chunk)
        #Update `start` para el siguiente fragmento, teniendo en cuenta el solapamiento
        start = end - overlap
        if start >= len(words):
            break
        pass

    return chunks
