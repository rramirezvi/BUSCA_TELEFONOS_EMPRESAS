from flask import Flask, request, render_template
import re
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


def buscar_numeros_empresa(empresa):
    # Realizar la búsqueda en Google
    query = f"{empresa} contacto"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    # Configurar headers para evitar bloqueos
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
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
    numeros = {"empresa": "", "numeros": []}  # Inicializar vacíos
    if request.method == "POST":
        empresa = request.form.get("empresa")
        if empresa:
            numeros = buscar_numeros_empresa(empresa)
    return render_template("index.html", numeros=numeros)


if __name__ == "__main__":
    app.run(debug=True)
