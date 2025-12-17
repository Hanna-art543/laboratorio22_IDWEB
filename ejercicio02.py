import requests

def listar_pokemons():
    
    params = {"limit": 10}
    url = "https://pokeapi.co/api/v2/pokemon"
    
    respuesta = requests.get(url, params=params)
    
    if respuesta.status_code == 200:
        resultados = respuesta.json().get('results', [])
        print("Primeros 10 Pokémon")
        for i, pokemon in enumerate(resultados, 1):
            print(f"{i}. {pokemon['name']}")
    else:
        print("No se pudo obtener la lista.")

if __name__ == "__main__":
    listar_pokemons()


    