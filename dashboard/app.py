import requests
from flask import Flask, jsonify, render_template
import os
API_URL = os.environ.get("API_URL", "http://api:5000/dados")

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/leitura")
def leitura():
    """O backend do dashboard consulta a API pela rede interna do Compose."""
    try:
        r = requests.get(API_URL, timeout=3)
        if r.status_code == 200:
            d = r.json()
            return jsonify({
                "disponivel": True,
                "temperatura": d["temperatura"],
                "umidade": d["umidade"],
                "estado": d["estado"],
            })
    except (requests.RequestException, ValueError, KeyError):
        pass
    return jsonify({"disponivel": False})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)