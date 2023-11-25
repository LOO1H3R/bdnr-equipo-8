#!/usr/bin/env python3
import csv
import requests

BASE_URL = "http://localhost:8000"

def insert_flight_passenger(passenger):
    response = requests.post(f"{BASE_URL}/flight_passenger", json=passenger)
    if not response.ok:
        print(f"Failed to post flight passenger {response.status_code} - {passenger}")

def insert_filtered_flight_info(passenger):
    passenger['capacidad_avion'] = 100
    passenger['connection'] = passenger['connection'].lower() == 'true'
    passenger['wait'] = int(passenger['wait'])

    if passenger['connection'] and passenger['wait'] > 60:
        response = requests.post(f"{BASE_URL}/vuelo_filtrado", json=passenger)
        if not response.ok:
            print(f"Failed to post filtered flight info {response.status_code} - {passenger}")

def main():
    with open("/home/guillermoclinux/bdnr-equipo-8/flight_passengers.csv") as fd:
        passengers_csv = csv.DictReader(fd)
        for passenger in passengers_csv:
            insert_flight_passenger(passenger)
            insert_filtered_flight_info(passenger)

if __name__ == "__main__":
    main()
