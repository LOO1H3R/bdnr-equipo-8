from random import choice, randint, randrange
from datetime import datetime, timedelta
import requests
import json

airlines = ["American Airlines", "Delta Airlines", "Alaska", "Aeromexico", "Volaris", "United Airlines", "British Airways", "Air France", "Emirates", "Qatar Airways", "Singapore Airlines", "Korean Air", "Japan Airlines", "Turkish Airlines", "LATAM Airlines", "Air Canada", "Copa Airlines"]
airports = ["PDX", "GDL", "SJC", "LAX", "JFK", "ORD", "LHR", "CDG", "DXB", "DOH", "SIN", "ICN", "NRT", "IST", "SCL", "YYZ", "PTY"]
genders = ["male", "female", "unspecified", "undisclosed"]
reasons = ["On vacation/Pleasure", "Business/Work", "Back Home"]
stays = ["Hotel", "Short-term homestay", "Home", "Friend/Family"]
transits = ["Airport cab", "Car rental", "Mobility as a service", "Public Transportation", "Pickup", "Own car"]
connections = [True, False]

# Función para generar fechas aleatorias
def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = randrange(days_between_dates)
    rand_date = start_date + timedelta(days=random_number_of_days)
    return rand_date

# URL de la API de Dgraph
dgraph_url = "http://localhost:8080/graphql"

# Datos de ejemplo
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

# Realizar 10 inserciones
for _ in range(10):
    flight_data = {
        "name": choice(airlines),
        "season": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        },
        "reason": choice(reasons),
        "duration": randint(0, 72)  # Duración en horas
    }

    airport_data = {
        "code": choice(airports),
        "location": {
            "city": "City",
            "country": "Country",
            "address": "Airport Address"
        },
        "flights": [flight_data]
    }

    # Construir la consulta GraphQL
    query = 'mutation { addAirport(input: ' + json.dumps(airport_data) + ') { airport { code } } }'
    #print(query)
    # Convertir los datos a formato JSON
    json_data = {"query": query}
    print(json_data)
    # Realizar la solicitud HTTP
    response = requests.post(dgraph_url, json=json_data)

    # Imprimir la respuesta
    #print(response.json())