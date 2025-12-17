from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class MiServidor(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = "<html><body><h1>Bienvenido al Servidor</h1></body></html>"
            self.wfile.write(html.encode())
            
        elif self.path == "/saludo":

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            data = {"msg": "Hola"}
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_error(404, "Ruta no encontrada")

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), MiServidor)
    print("Servidor en http://localhost:8000")
    server.serve_forever()

    