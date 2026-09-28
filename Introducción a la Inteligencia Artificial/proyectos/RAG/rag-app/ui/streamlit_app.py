# ui/streamlit_app.py
import uuid
import requests
import streamlit as st
import io
from pypdf import PdfReader

API_URL = "http://localhost:8000"

GEMINI_MODELS = ["gemini-3.6-flash", "gemini-3.7-flash", "gemini-3.8-flash"]

# ---------------------------------------------------------------------------
# Estado de sesión
# ---------------------------------------------------------------------------
def nuevo_id() -> str:
    return str(uuid.uuid4())[:8]
 
 
if "chats" not in st.session_state:
    cid = nuevo_id()
    st.session_state.chats = {cid: {"title": "Nuevo chat", "messages": []}}
    st.session_state.current = cid
 
 
def chat_actual() -> dict:
    return st.session_state.chats[st.session_state.current]
 
# ---------------------------------------------------------------------------
# Llamadas a la API 
# ---------------------------------------------------------------------------
def api_viva() -> bool:
    try:
        return requests.get(f"{API_URL}/health", timeout=3).status_code == 200
    except Exception:
        return False

def leer_texto(archivo) -> str:
    """Extrae el texto de un archivo subido (.txt, .md o .pdf)."""
    if archivo.name.lower().endswith(".pdf"):
        lector = PdfReader(io.BytesIO(archivo.getvalue()))
        paginas = [(pagina.extract_text() or "") for pagina in lector.pages]
        return "\n".join(paginas).strip()
    # .txt / .md
    return archivo.getvalue().decode("utf-8") 
 
def ingerir(archivo) -> dict:
    texto = leer_texto(archivo)
    if not texto.strip():
        # PDF escaneado (solo imagen) o archivo vacío: no hay texto que indexar
        raise ValueError("sin texto extraíble (¿PDF escaneado? necesitaría OCR)")
    resp = requests.post(
        f"{API_URL}/ingest",
        json={"text": texto, "source": archivo.name},
        timeout=120,
    )
    return resp.json()
 
 
def consultar(pregunta: str, top_k: int, model: str) -> dict:
    resp = requests.post(
        f"{API_URL}/query",
        json={"question": pregunta, "top_k": top_k, "model": model},
        timeout=180, # tiempo extendido para preguntas largas o modelos más lentos
    )
    return resp.json()

# ---------------------------------------------------------------------------
# Barra lateral: estado de la API, configuración e historial de chats
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuración")
 
    if api_viva():
        st.success("API conectada (:8000)")
    else:
        st.error("API no disponible. Levanta FastAPI en el puerto 8000.")
 
    model = st.selectbox("Modelo de generación", GEMINI_MODELS)
    top_k = st.slider("Fragmentos a recuperar (top-k)", 1, 5, 3)
 
    st.divider()
 
    if st.button("➕ Nuevo chat", use_container_width=True):
        cid = nuevo_id()
        st.session_state.chats[cid] = {"title": "Nuevo chat", "messages": []}
        st.session_state.current = cid
        st.rerun()
 
    st.caption("Historial de la sesión")
    for cid, chat in st.session_state.chats.items():
        marca = "🟢 " if cid == st.session_state.current else ""
        if st.button(marca + chat["title"], key=f"chat_{cid}", use_container_width=True):
            st.session_state.current = cid
            st.rerun()
            
# ---------------------------------------------------------------------------
# Área principal: título + render del historial del chat actual
# ---------------------------------------------------------------------------
st.title("Bienvenido a BBVA 🏦")
st.caption("Preguntas ancladas en el corpus, con citas y scores. Adjunta .txt/.md para indexar.")
 
 
def render_mensaje(msg: dict) -> None:
    with st.chat_message(msg["role"]):
        estado = msg.get("estado", "ok")
        if estado == "abstenido":
            st.warning(msg["content"])
        elif estado == "error":
            st.error(msg["content"])
        elif estado == "info":
            st.info(msg["content"])
        else:
            st.markdown(msg["content"])
 
        # Citas (chunks recuperados con origen + score)
        for i, c in enumerate(msg.get("citations", []), start=1):
            with st.expander(f"[{i}] {c['source']} — score {c['score']:.3f}"):
                st.write(c["text"])
 
 
for msg in chat_actual()["messages"]:
    render_mensaje(msg)
    
# ---------------------------------------------------------------------------
# Entrada de chat con adjuntos
# ---------------------------------------------------------------------------
entrada = st.chat_input(
    "Escribe tu pregunta o adjunta documentos ...",
    accept_file="multiple",
    file_type=["txt", "md", "pdf"],
)
 
if entrada:
    # 1) Adjuntos -> indexar vía /ingest
    if entrada.files:
        lineas = []
        for archivo in entrada.files:
            try:
                data = ingerir(archivo)
                lineas.append(f"**{data['source']}** → {data['chunks_indexed']} chunks")
            except Exception as e:
                lineas.append(f"**{archivo.name}** → error: {e}")
        chat_actual()["messages"].append(
            {"role": "assistant", "estado": "info",
             "content": "📄 Documentos indexados:\n\n" + "\n\n".join(lineas)}
        )
 
    # 2) Texto -> consultar vía /query
    if entrada.text and entrada.text.strip():
        pregunta = entrada.text.strip()
        chat_actual()["messages"].append({"role": "user", "content": pregunta})
 
        # El título del chat toma la primera pregunta (para el historial lateral)
        if chat_actual()["title"] == "Nuevo chat":
            chat_actual()["title"] = pregunta[:30] + ("…" if len(pregunta) > 30 else "")
 
        with st.spinner("Recuperando evidencia y generando…"):
            try:
                data = consultar(pregunta, top_k, model)
            except Exception as e:
                data = None
                chat_actual()["messages"].append(
                    {"role": "assistant", "estado": "error",
                     "content": f"No se pudo conectar con la API: {e}"}
                )
 
        if data is not None:
            if data.get("error"):
                estado = "error"
            elif data.get("abstained"):
                estado = "abstenido"
            else:
                estado = "ok"
            chat_actual()["messages"].append(
                {"role": "assistant", "estado": estado,
                 "content": data["answer"], "citations": data.get("citations", [])}
            )
 
    st.rerun()    