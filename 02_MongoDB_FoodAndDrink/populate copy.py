#!/usr/bin/env python3
import csv
import requests

BASE_URL = "http://localhost:8000"

def insert_flight_passenger(passenger):
    response = requests.post(BASE_URL+"/recomendacion_restaurantes/FlightPassenger", json=passenger)
    if not response.ok:
        print(f"Failed to post flight passenger {response.status_code} - {passenger}")

def insert_filtered_flight_info(passenger):
    passenger['connection'] = passenger['connection'].lower() == 'true'
    passenger['wait'] = int(passenger['wait'])

    if passenger['connection'] and passenger['wait'] > 60:
        response = requests.post(BASE_URL+"/recomendacion_restaurantes/AeropuertosMayorEspera", json=passenger)
        if not response.ok:
            print(f"Failed to post filtered flight info {response.status_code} - {passenger}")

def insert_restaurant(restaurant):
    restaurant['rating'] = float(restaurant['rating'])  # Convertir rating a float
    restaurant['opinions'] = restaurant['opinions'].split(',')
    
    response = requests.post(BASE_URL+"/recomendacion_restaurantes/RecomendacionAlimentoBebida", json=restaurant)
    if not response.ok:
        print(f"Failed to post restaurant data {response.status_code} - {restaurant}")

def main():
    # Insert flight passengers
    with open("/home/guillermoclinux/iteso-bdnr-pruebas/data/flight_passengers.csv") as fd:
        passengers_csv = csv.DictReader(fd)
        for passenger in passengers_csv:
            insert_flight_passenger(passenger)
            insert_filtered_flight_info(passenger)
    
    # Insert restaurants
    with open("/home/guillermoclinux/iteso-bdnr-pruebas/data/restaurantes.csv") as fd:
        restaurants_csv = csv.DictReader(fd)
        for restaurant in restaurants_csv:
            insert_restaurant(restaurant)

if __name__ == "__main__":
    main()
