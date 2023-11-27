#!/usr/bin/env python

"""
Generador de datos para restaurantes en aeropuertos
"""

import csv
import random

# Datos predefinidos
airports = ["PDX", "GDL", "SJC", "LAX", "JFK"]
restaurant_names = ["Tacos Campeche", "Burger House", "Sushi World", "Pasta Paradise", "Veggie Delight"]
cuisine_types = ["Mexicana", "Americana", "Japonesa", "Italiana", "Vegetariana"]
price_ranges = ["100-200", "200-300", "300-600", "600-900"]
opinion_samples = ["Delicioso", "Buen servicio", "Poco caro, pero son rápidos", "Recomendable", "No me gustó", "Excelente ambiente"]

# Función para generar opiniones aleatorias
def generate_opinions():
    opinions = []
    for _ in range(random.randint(1, 3)):  # Generar entre 1 y 3 opiniones
        opinions.append(random.choice(opinion_samples))
    return opinions

# Función para generar el conjunto de datos
def generate_restaurant_dataset(output_file, rows):
    with open(output_file, "w", newline='', encoding='utf-8') as fd:
        fieldnames = ["airport", "restaurant_name", "cuisine_type", "price_range", "rating", "opinions"]
        writer = csv.DictWriter(fd, fieldnames=fieldnames)
        writer.writeheader()
        for _ in range(rows):
            restaurant_data = {
                "airport": random.choice(airports),
                "restaurant_name": random.choice(restaurant_names),
                "cuisine_type": random.choice(cuisine_types),
                "price_range": random.choice(price_ranges),
                "rating": round(random.uniform(1.0, 5.0), 1),  # Calificación entre 1.0 y 5.0
                "opinions": generate_opinions()
            }
            writer.writerow(restaurant_data)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Output filename, defaults to: restaurantes.csv", default="restaurantes.csv")
    parser.add_argument("-r", "--rows", help="Number of entries to generate, defaults to: 1000", type=int, default=1000)
    args = parser.parse_args()

    print(f"Generating {args.rows} entries for restaurant dataset")
    generate_restaurant_dataset(args.output, args.rows)
    print(f"Completed generating dataset in {args.output}")
