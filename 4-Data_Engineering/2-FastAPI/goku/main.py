import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


class ChatMessage(BaseModel):
    mensaje: str


@app.get("/hola")
def hola_mundo():
    return {"mensaje": "Hola mundo"}


@app.post("/chat")
def chat_goku(msg: ChatMessage):

    prompt = f"""
    Actúa como Goku de Dragon Ball. Responde siempre como él, 
    alegre, poderoso y motivador. No rompas el personaje.

    Usuario: {msg.mensaje}
    """

    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    # FIX del error
    texto_respuesta = respuesta.choices[0].message.content

    return {"respuesta": texto_respuesta}


@app.get("/", response_class=HTMLResponse)
def pagina_principal():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8" />
        <title>Chat con Goku</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(120deg, #ff9800, #ff5722);
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                color: white;
            }

            #chat-container {
                width: 90%;
                max-width: 600px;
                background: rgba(255, 255, 255, 0.15);
                padding: 20px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                box-shadow: 0 0 20px rgba(0,0,0,0.3);
            }

            h1 {
                text-align: center;
                margin-top: 0;
            }

            #messages {
                height: 300px;
                overflow-y: auto;
                background: rgba(0,0,0,0.2);
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 10px;
            }

            .msg {
                margin: 8px 0;
                padding: 10px;
                border-radius: 10px;
                max-width: 80%;
            }

            .user {
                background: #4caf50;
                margin-left: auto;
            }

            .goku {
                background: #2196f3;
                margin-right: auto;
            }

            #input-box {
                display: flex;
            }

            #mensaje {
                flex: 1;
                padding: 10px;
                border-radius: 8px;
                border: none;
                outline: none;
                font-size: 16px;
            }

            button {
                margin-left: 10px;
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                background: #673ab7;
                color: white;
                cursor: pointer;
                font-size: 16px;
            }

            button:hover {
                background: #5e35b1;
            }
        </style>
    </head>
    <body>

        <div id="chat-container">
            <h1>Chat con Goku 🐉</h1>

            <div id="messages"></div>

            <div id="input-box">
                <input id="mensaje" type="text" placeholder="Escribe algo para Goku..." />
                <button onclick="enviar()">Enviar</button>
            </div>
        </div>

        <script>
            const messagesDiv = document.getElementById("messages");

            function agregarMensaje(texto, clase) {
                const div = document.createElement("div");
                div.className = "msg " + clase;
                div.textContent = texto;
                messagesDiv.appendChild(div);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }

            async function enviar() {
                const texto = document.getElementById("mensaje").value;
                if (!texto) return;

                agregarMensaje(texto, "user");

                const resp = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ mensaje: texto })
                });

                const data = await resp.json();
                agregarMensaje(data.respuesta, "goku");

                document.getElementById("mensaje").value = "";
            }

            // Enviar con Enter
            document.getElementById("mensaje").addEventListener("keypress", function(e) {
                if (e.key === "Enter") enviar();
            });
        </script>

    </body>
    </html>
    """
