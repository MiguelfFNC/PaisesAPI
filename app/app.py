from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder="templates", static_folder="static")


def obtener_paises():
    try:
        cabecera = {"User-Agent": "Mozilla/5.0"}
        respuesta_api = requests.get(
            "https://restcountries.com/v3.1/all?fields=translations,flags,capital,region,subregion,population,area,languages,currencies",
            headers=cabecera, timeout=10
        )
        respuesta_api.raise_for_status()
        Datos_Paises = respuesta_api.json()
        paises_validos = []
        for paises in Datos_Paises:
            if "name" in paises and "common" in paises["name"]:
                paises_validos.append(paises)
        return paises_validos
    except Exception as e:
        print("Error al cargar los países:", e)
        return []


@app.route("/autocompletado")
def autocompletado():
    query = request.args.get("q", "").lower()
    paises = obtener_paises()
    coincidencias = []
    for pais in paises:
        if pais["name"]["common"].lower().startswith(query):
            coincidencias.append(pais["name"]["common"])
    return jsonify(coincidencias[:10])


@app.route("/busqueda")
def busqueda():
    nombre_pais = request.args.get("country")
    if not nombre_pais:
        return jsonify({"error": "no se ingreso ningun pais"}), 400
    paises = obtener_paises()
    coincidencias = []
    for pais in paises:
        if pais["name"]["common"].lower() == nombre_pais.lower():
            coincidencias.append(pais)
    if not coincidencias:
        return jsonify({"error": "pais no encontrado"}), 404

    datos = coincidencias[0]
    nombre = datos["name"]["common"]
    bandera = datos["flags"]["svg"]
    capital = datos.get("capital", [""])[0]
    region = datos.get("region", [""])
    poblacion = f"{datos.get('population', 0):,}"
    area = f"{datos.get('area', 0):,} km²"

    idiomas = ""
    if datos.get("languages"):
        idiomas = ", ".join(datos["languages"].values())

    moneda = ""
    if "currencies" in datos:
        informacion_moneda = next(iter(datos["currencies"].values()))
        nombre_moneda = informacion_moneda.get("name", "")
        simbolo_moneda = informacion_moneda.get("symbol", "")
        moneda = f"{nombre_moneda}({simbolo_moneda})"

    resultado = {
        "name": nombre,
        "flag": bandera,
        "capital": capital,
        "region": region,
        "population": poblacion,
        "area": area,
        "languages": idiomas,
        "currencies": moneda
    }
    return jsonify(resultado)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=7000)
