import csv
import uuid
import logging

# Configuración del logger
logging.basicConfig(filename='generador.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

def generar_commando_insert_cql_datos_completos(csv_file, cql_file):
    try:
        with open(csv_file, newline='') as csvfile, open(cql_file, 'w') as cqlfile:
            reader = csv.DictReader(csvfile)
            passenger_counts = {}

            for row in reader:
                flight_key = (row['airline'], row['from'], row['to'])
                passenger_counts[flight_key] = passenger_counts.get(flight_key, 0) + 1

            for flight_key, count in passenger_counts.items():
                aerolinea, desde, hacia = flight_key
                id_vuelo = uuid.uuid4()
                capacidad = 100
                cqlfile.write(f"INSERT INTO datos_pasajero_vuelo (id_vuelo, aerolinea, desde, hacia, capacidad, recuento_pasajeros) VALUES ({id_vuelo}, '{aerolinea}', '{desde}', '{hacia}', {capacidad}, {count});\n")

        logging.info("Archivo CQL generado con éxito.")
    except Exception as e:
        logging.error(f"Error al generar el archivo CQL: {e}")

def generar_commando_insert_cql_datos_filtrados(csv_file, cql_file, max_pasajeros):
    try:
        with open(csv_file, newline='') as csvfile, open(cql_file, 'w') as cqlfile:
            reader = csv.DictReader(csvfile)
            passenger_counts = {}

            for row in reader:
                flight_key = (row['airline'], row['from'], row['to'])
                passenger_counts[flight_key] = passenger_counts.get(flight_key, 0) + 1

            for flight_key, count in passenger_counts.items():
                if count <= max_pasajeros:
                    aerolinea, desde, hacia = flight_key
                    id_vuelo = uuid.uuid4()
                    capacidad = 100
                    cqlfile.write(f"INSERT INTO rutas_menos_transitadas (id_vuelo, aerolinea, desde, hacia, capacidad, recuento_pasajeros) VALUES ({id_vuelo}, '{aerolinea}', '{desde}', '{hacia}', {capacidad}, {count});\n")

        logging.info("Archivo CQL generado con éxito.")
    except Exception as e:
        logging.error(f"Error al generar el archivo CQL: {e}")


if __name__ == '__main__':
    csv_path = "/home/guillermoclinux/bdnr-equipo-8-public/data/flight_passengers.csv"
    cql_path = "/home/guillermoclinux/bdnr-equipo-8/Cassandra Model 3/datos_pasajero_vuelo.cql"
    generar_commando_insert_cql_datos_completos(csv_path, cql_path)
