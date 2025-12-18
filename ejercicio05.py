from wsgiref.simple_server import make_server

def aplicacion_wsgi(environ, start_response):
    ruta = environ.get("PATH_INFO", "/")
    if ruta == "/":
        status = "200 OK"
        respuesta = b"Inicio"
    elif ruta == "/saludo":
        status = "200 OK"
        respuesta = b"Hola mundo desde WSGI"
    else:
        status = "404 Not Found"
        respuesta = b"No encontrado"
    
    headers = [("Content-Type", "text/plain")]
    start_response(status, headers)
    return [respuesta]

if __name__ == "__main__":
    server = make_server("localhost", 8000, aplicacion_wsgi)
    print("WSGI en http://localhost:8000")
    server.serve_forever()

