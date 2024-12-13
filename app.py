from flask import Flask, request, render_template
import re
import requests
import random
from bs4 import BeautifulSoup


app = Flask(__name__)

# Lista de User-Agents para alternar
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Mobile/15E148",
    "Mozilla/5.0 (Android 10; Mobile; rv:90.0) Gecko/90.0 Firefox/90.0"
]


def buscar_numeros_empresa(empresa):
    # Realizar la búsqueda en Google
    query = f"{empresa} contacto"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    # Seleccionar un User-Agent aleatorio
    user_agent = random.choice(USER_AGENTS)

    # Configurar headers para evitar bloqueos
    # Configurar headers con User-Agent seleccionado
    headers = {
        "User-Agent": user_agent
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscar números de teléfono con regex
    pattern = re.compile(r'\(?\d{2,4}\)?[-.\s]?\d{3}[-.\s]?\d{3,4}')
    numeros = pattern.findall(soup.text)

    # Eliminar duplicados
    return {"empresa": empresa, "numeros": list(set(numeros))}


@app.route("/", methods=["GET", "POST"])
def index():
    numeros = None  # Inicializar vacíos
    if request.method == "POST":
        empresa = request.form.get("empresa")
        if empresa:
            numeros = buscar_numeros_empresa(empresa)
    return render_template("index.html", numeros=numeros)


if __name__ == "__main__":
    app.run(debug=True)
