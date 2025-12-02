import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Obtener API key desde el .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inicializar OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

# ---- MODELO PARA EL CHAT ----
class ChatMessage(BaseModel):
    mensaje: str


# ---- ENDPOINT HOLA MUNDO ----
@app.get("/hola")
def hola_mundo():
    return {"mensaje": "Hola mundo"}


# ---- ENDPOINT CHATBOT CON OPENAI (Goku) ----
@app.post("/chat")
def chat_goku(msg: ChatMessage):

    prompt = f"""
    Actúa como Goku de Dragon Ball. Responde con entusiasmo
    y nunca rompas el personaje.
    Usuario: {msg.mensaje}
    """

    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    texto_respuesta = respuesta.choices[0].message["content"]

    return {"respuesta": texto_respuesta}


# ---- HTML MUY BÁSICO ----
@app.get("/", response_class=HTMLResponse)
def pagina_principal():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"><title>Chat Goku</title></head>
    <body>
        <h1>Chat con Goku (OpenAI + .env)</h1>
        <input id="mensaje" type="text" placeholder="Escribe algo..." />
        <button onclick="enviar()">Enviar</button>
        <h2>Respuesta:</h2>
        <pre id="respuesta"></pre>

        <script>
            async function enviar() {
                const texto = document.getElementById("mensaje").value;
                const resp = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ mensaje: texto })
                });
                const data = await resp.json();
                document.getElementById("respuesta").textContent = data.respuesta;
            }
        </script>
    </body>
    </html>
    """
