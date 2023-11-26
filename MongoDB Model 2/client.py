#!/usr/bin/env python3
import argparse
import logging
import os
import requests
import json

# Configuración del logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('client.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Leer variables de entorno para la conexión con la API
API_URL = os.getenv("API_URL", "http://localhost:8000")

def handle_response(response):
    """ Maneja la respuesta de la API, imprimiendo el resultado o el error. """
    if response.ok:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")

def get_recomendaciones(aeropuerto):
    try:
        response = requests.get(f"{API_URL}/recomendaciones/aeropuerto/{aeropuerto}")
        recomendaciones = handle_response(response)
        if recomendaciones:
            for rec in recomendaciones:
                print(json.dumps(rec, indent=4))
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")

def find_recomendaciones(tipo_cocina, calificacion_minima):
    try:
        params = {"tipo_cocina": tipo_cocina, "calificacion_minima": calificacion_minima}
        response = requests.get(f"{API_URL}/recomendaciones/buscar", params=params)
        recomendaciones = handle_response(response)
        if recomendaciones:
            for rec in recomendaciones:
                print(json.dumps(rec, indent=4))
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")

def update_calificacion(id_recomendacion, nueva_calificacion):
    try:
        data = {"calificacion": nueva_calificacion}
        response = requests.put(f"{API_URL}/recomendaciones/{id_recomendacion}/calificacion", json=data)
        resultado = handle_response(response)
        if resultado:
            print("Calificación actualizada con éxito.")
            print(json.dumps(resultado, indent=4))
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")

def insertar_opinion(id_recomendacion, opinion):
    try:
        data = {"opinion": opinion}
        response = requests.post(f"{API_URL}/recomendaciones/{id_recomendacion}/opinion", json=data)
        resultado = handle_response(response)
        if resultado:
            print("Opinión insertada con éxito.")
            print(json.dumps(resultado, indent=4))
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")

def eliminar_opinion(id_recomendacion, id_opinion):
    try:
        response = requests.delete(f"{API_URL}/recomendaciones/{id_recomendacion}/opinion/{id_opinion}")
        resultado = handle_response(response)
        if resultado:
            print("Opinión eliminada con éxito.")
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")

def main():
    parser = argparse.ArgumentParser(description="Cliente API de recomendaciones de alimentos y bebidas")

    parser.add_argument("--get", help="Obtener recomendaciones para un aeropuerto específico", type=str)
    parser.add_argument("--find", nargs=2, help="Buscar recomendaciones por tipo de cocina y calificación mínima", metavar=('TIPO_COCINA', 'CALIFICACION_MINIMA'))
    parser.add_argument("--update", nargs=2, help="Actualizar la calificación de una recomendación", metavar=('ID_RECOMENDACION', 'NUEVA_CALIFICACION'))
    parser.add_argument("--insert", nargs=2, help="Insertar una nueva opinión", metavar=('ID_RECOMENDACION', 'OPINION'))
    parser.add_argument("--delete", nargs=2, help="Eliminar una opinión específica", metavar=('ID_RECOMENDACION', 'ID_OPINION'))

    args = parser.parse_args()

    # Manejo de argumentos de la línea de comandos
    if args.get:
        get_recomendaciones(args.get)
    elif args.find:
        tipo_cocina, calificacion_minima = args.find
        find_recomendaciones(tipo_cocina, float(calificacion_minima))
    elif args.update:
        id_recomendacion, nueva_calificacion = args.update
        update_calificacion(id_recomendacion, float(nueva_calificacion))
    elif args.insert:
        id_recomendacion, opinion = args.insert
        insertar_opinion(id_recomendacion, opinion)
    elif args.delete:
        id_recomendacion, id_opinion = args.delete
        eliminar_opinion(id_recomendacion, id_opinion)

if __name__ == "__main__":
    main()