import json
from wsgiref.simple_server import make_server

biblioteca = [
    {"id": 1, "titulo": "1984", "autor": "George Orwell", "anio": 1949}
]
id_actual = 1

def app_libros(environ, start_response):
    global id_actual
    metodo = environ["REQUEST_METHOD"]
    ruta = environ["PATH_INFO"]
    
    # a) Listar libros
    if metodo == "GET" and ruta == "/libros":
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(biblioteca).encode()]
    
    # b) Registrar nuevo 
    elif metodo == "POST" and ruta == "/libros":
        longitud = int(environ.get("CONTENT_LENGTH", 0))
        cuerpo = environ["wsgi.input"].read(longitud)
        nuevo_datos = json.loads(cuerpo)
        
        id_actual += 1
        nuevo_libro = {
            "id": id_actual,
            "titulo": nuevo_datos["titulo"],
            "autor": nuevo_datos["autor"],
            "anio": nuevo_datos["anio"]
        }
        biblioteca.append(nuevo_libro)
        
        start_response("201 Created", [("Content-Type", "application/json")])
        return [json.dumps(nuevo_libro).encode()]

    # c) Consultar por ID 
    elif metodo == "GET" and ruta.startswith("/libros/"):
        try:
            libro_id = int(ruta.split("/")[-1])
            libro = next((l for l in biblioteca if l["id"] == libro_id), None)
            
            if libro:
                start_response("200 OK", [("Content-Type", "application/json")])
                return [json.dumps(libro).encode()]
            else:
                start_response("404 Not Found", [("Content-Type", "text/plain")])
                return [b"Libro no encontrado"] 
        except ValueError:
            start_response("400 Bad Request", [("Content-Type", "text/plain")])
            return [b"ID invalido"]

    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Ruta no encontrada"]

if __name__ == "__main__":
    server = make_server("localhost", 8000, app_libros)
    print("Servidor de Libros en http://localhost:8000/libros")
    server.serve_forever()