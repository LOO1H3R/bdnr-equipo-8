import requests
import json

# URL de la API de Dgraph
dgraph_url = "http://localhost:8080/graphql"

# Datos de ejemplo para la mutación
mutation_data = {
    "query": 'mutation { addAirport(input: {code: "JFK", location: {city: "New York", country: "USA", address: "JFK Airport"}, flights: [{name: "American Airlines", season: {start_date: "2023-01-01T00:00:00Z", end_date: "2023-12-31T23:59:59Z"}, reason: "Back Home", duration: 23}]} ) { airport { code } } }'
}

# Realizar la solicitud HTTP
response = requests.post(dgraph_url, json=mutation_data)

# Imprimir la respuesta
print(response.json())