import json, os, mimetypes
from wsgiref.simple_server import make_server
from urllib.parse import unquote

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

equipos = [
    {"id": 1, "nombre": "Real Madrid", "ciudad": "Madrid", "nivelAtaque": 10, "nivelDefensa": 9},
    {"id": 2, "nombre": "Barcelona", "ciudad": "Barcelona", "nivelAtaque": 9, "nivelDefensa": 8},
    {"id": 3, "nombre": "Melgar", "ciudad": "Arequipa", "nivelAtaque": 5, "nivelDefensa": 4}
]

id_equipo_actual = 3

def servir_estatico(path):
    nombre_archivo = path.replace("/static/", "").lstrip("/")
    full_path = os.path.join(STATIC_DIR, nombre_archivo)

    if not os.path.isfile(full_path):
        return None, None

    tipo, _ = mimetypes.guess_type(full_path)
    
    if full_path.endswith(".css"):
        tipo = "text/css"
    elif full_path.endswith(".js"):
        tipo = "application/javascript"
    elif full_path.endswith(".html"):
        tipo = "text/html"
    
    tipo = tipo or "application/octet-stream"

    with open(full_path, "rb") as f:
        return f.read(), tipo

def app_avanzada(environ, start_response):
    global id_equipo_actual
    metodo = environ.get("REQUEST_METHOD", "GET")
    path = unquote(environ.get("PATH_INFO", "/"))

    if path.startswith("/static/"):
        contenido, tipo = servir_estatico(path)
        if contenido:
            start_response("200 OK", [("Content-Type", f"{tipo}; charset=utf-8")])
            return [contenido]

    if path.endswith(".css") or path.endswith(".js"):
        contenido, tipo = servir_estatico(path)
        if contenido:
            start_response("200 OK", [("Content-Type", f"{tipo}; charset=utf-8")])
            return [contenido]

    
    if metodo == "GET" and path == "/":
        contenido, tipo = servir_estatico("index.html")
        if contenido:
            start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
            return [contenido]

    if path == "/equipos":
        if metodo == "GET":
            start_response("200 OK", [("Content-Type", "application/json; charset=utf-8")])
            return [json.dumps(equipos).encode("utf-8")]
        
        elif metodo == "POST":
            longitud = int(environ.get("CONTENT_LENGTH") or 0)
            cuerpo = environ["wsgi.input"].read(longitud)
            data = json.loads(cuerpo.decode("utf-8"))
            
            id_equipo_actual += 1
            nuevo = {
                "id": id_equipo_actual,
                "nombre": data.get("nombre"),
                "ciudad": data.get("ciudad"),
                "nivelAtaque": data.get("nivelAtaque"),
                "nivelDefensa": data.get("nivelDefensa")
            }
            equipos.append(nuevo)
            start_response("201 Created", [("Content-Type", "application/json; charset=utf-8")])
            return [json.dumps(nuevo).encode("utf-8")]

    if path.startswith("/equipos/"):
        try:
            eq_id = int(path.split("/")[-1])
            equipo = next((e for e in equipos if e["id"] == eq_id), None)
            if equipo:
                start_response("200 OK", [("Content-Type", "application/json; charset=utf-8")])
                return [json.dumps(equipo).encode("utf-8")]
        except ValueError:
            pass

    start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
    return [b"No encontrado"]

if __name__ == "__main__":
    server = make_server("localhost", 8000, app_avanzada)
    print("Servidor listo en http://localhost:8000")
    server.serve_forever()