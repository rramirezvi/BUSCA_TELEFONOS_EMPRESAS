import re
import requests
from bs4 import BeautifulSoup


def buscar_numeros_empresa(empresa):
    # Realizar la búsqueda en un motor de búsqueda
    query = f"{empresa} contacto"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    # Configurar headers para evitar bloqueos
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscar números de teléfono con regex
    pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
    numeros = pattern.findall(soup.text)

    # Eliminar duplicados
    return list(set(numeros))


empresa = "Holcim pedernales"
numeros = buscar_numeros_empresa(empresa)
print("Números encontrados:", numeros)
