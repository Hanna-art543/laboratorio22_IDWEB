
import requests

def consultar_httpbin():
    url = "https://httpbin.org/get"
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200:
        datos = respuesta.json() 
        print("--- Datos de la Petición ---")
        print(f"IP (Origin): {datos.get('origin')}")
        print(f"Headers: {datos.get('headers')}")
        print(f"Args: {datos.get('args')}")
    else:
        print(f"Error en la petición: {respuesta.status_code}")

if __name__ == "__main__":
    consultar_httpbin()