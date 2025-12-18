from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class SumadorHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sumador POST</title>
        </head>
        <body>
            <h2>Sumador usando POST</h2>
            <input type="number" id="a" placeholder="Numero A"><br><br>
            <input type="number" id="b" placeholder="Numero B"><br><br>
            <button onclick="sumar()">Sumar</button>
            <p id="resultado"></p>

            <script>
                function sumar() {
                    fetch("/", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            a: document.getElementById("a").value,
                            b: document.getElementById("b").value
                        })
                    })
                    .then(res => res.json())
                    .then(data => {
                        document.getElementById("resultado").innerText =
                            "La suma es: " + data.suma;
                    });
                }
            </script>
        </body>
        </html>
        """)

    def do_POST(self):

        longitud = int(self.headers.get("Content-Length", 0))
        cuerpo = self.rfile.read(longitud)
        datos = json.loads(cuerpo)
        
        a = int(datos.get("a", 0))
        b = int(datos.get("b", 0))
        resultado = {"suma": a + b}
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(resultado).encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), SumadorHandler)
    print("Servidor de suma en puerto 8000")
    server.serve_forever()


