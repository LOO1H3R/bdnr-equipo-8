#!/usr/bin/env python3
import argparse
import logging
import os
import requests

# Set up logging
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('comida_bebidas.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read environment variables for API connection
FLIGHT_API_URL = os.getenv("API_URL", "http://localhost:8000")

def print_data(data):
    print(json.dumps(data, indent=4))
    print("=" * 50)

# Functions for RecomendacionAlimentoBebida
def list_restaurants(airport):
    endpoint = f"{API_URL}/RecomendacionAlimentoBebida"
    params = {"airport": airport}
    response = requests.get(endpoint, params=params)
    if response.ok:
        for restaurant in response.json():
            print_data(restaurant)
    else:
        print(f"Error: {response}")

def update_restaurant(id, data):
    endpoint = f"{API_URL}/RecomendacionAlimentoBebida/{id}"
    response = requests.put(endpoint, json=data)
    if response.ok:
        print("Restaurant updated successfully")
    else:
        print(f"Error updating restaurant: {response}")

# Functions for AeropuertosMayorEspera
def list_recommended_airports(wait):
    endpoint = f"{API_URL}/AeropuertosMayorEspera"
    params = {"wait": wait}
    response = requests.get(endpoint, params=params)
    if response.ok:
        for airport in response.json():
            print_data(airport)
    else:
        print(f"Error: {response}")

def main():
    log.info(f"Connecting to API at: {API_URL}")

    parser = argparse.ArgumentParser(description="Cliente de recomendación de restaurantes")
    parser.add_argument("entity", choices=["restaurant", "recommended_airport"], help="Entity to manage")
    parser.add_argument("action", choices=["list", "update"], help="Action to be performed")
    parser.add_argument("-i", "--id", help="ID for update action", default=None)
    parser.add_argument("-a", "--airport", help="Airport code for listing restaurants or recommended airports", default="")
    parser.add_argument("-w", "--wait", help="Minimum wait time for listing recommended airports", type=int, default=0)
    parser.add_argument("-d", "--data", help="Data for updating a restaurant in JSON format", default="{}")

    args = parser.parse_args()

    if args.entity == "restaurant":
        if args.action == "list":
            list_restaurants(args.airport)
        elif args.action == "update" and args.id:
            data = json.loads(args.data)
            update_restaurant(args.id, data)

    elif args.entity == "recommended_airport":
        if args.action == "list":
            list_recommended_airports(args.wait)

if __name__ == "__main__":
    main()
    