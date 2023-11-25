#!/usr/bin/env python3
import logging
import os
from datetime import datetime
import csv

from cassandra.cluster import Cluster

import model
import populate
import uuid


# Configuración del logger de las rutas
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('rutas_promocionales.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Configuración del logger del generador
logging.basicConfig(filename='generador.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')

# Leer variables de entorno relacionadas con la aplicación Cassandra
CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'promociones_vuelos')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')

def print_menu():
    mm_options = {
        1: "Crear o actualizar tabla con rutas menos transitadas",
        2: "Agregar ruta menos transitada",
        3: "Consultar rutas con N o menos pasajeros en toda la base de datos",
        4: "Mostrar rutas menos transitadas de una aerolínea en toda la base de datos",
        5: "Eliminar ruta menos transitada",
        6: "Agregar promoción",
        7: "Listar promociones",
        8: "Eliminar promoción",
        9: "Salir"
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def main():
    log.info("Conectando al cluster de Cassandra")
    cluster = Cluster(CLUSTER_IPS.split(','))
    session = cluster.connect()

    model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)

    model.create_schema(session)

    while True:
        print_menu()
        option = int(input('Ingrese su elección: '))
        if option == 1:
            max_pasajeros = int(input("Ingrese el número máximo de pasajeros con el que desea generar la tabla: "))
            csv_path = "/home/guillermoclinux/bdnr-equipo-8/flight_passengers.csv"
            cql_path1 = "/home/guillermoclinux/bdnr-equipo-8/Cassandra Model 3/rutas_menos_transitadas.cql"
            populate.generar_commando_insert_cql_datos_filtrados(csv_path, cql_path1, max_pasajeros)
        elif option == 2:
            aerolinea = input("Ingrese el nombre de la aerolínea: ")
            id_vuelo = uuid.uuid4()
            desde = input("Ingrese el origen del vuelo: ")
            hacia = input("Ingrese el destino del vuelo: ")
            capacidad = int(input("Ingrese la capacidad del vuelo: "))
            recuento_pasajeros = int(input("Ingrese el recuento actual de pasajeros: "))
            model.agregar_ruta_menos_transitada(session, aerolinea, id_vuelo, desde, hacia, capacidad, recuento_pasajeros)
                #print("Error al insertar la ruta. Intente de nuevo.")
                #continue
        elif option == 3:
            max_pasajeros = int(input("Ingrese el número máximo de pasajeros: "))
            model.consultar_rutas_con_menos_pasajeros(session, max_pasajeros)
        elif option == 4:
            aerolinea = input('Ingrese el nombre de la aerolínea: ')
            max_pasajeros = int(input("Ingrese el número máximo de pasajeros: "))
            model.get_rutas_por_pasajeros_aerolinea(session, aerolinea, max_pasajeros)
        elif option == 5:
            aerolinea = input("Ingrese el nombre de la aerolínea para la ruta a eliminar: ")
            id_vuelo = uuid.UUID(input("Ingrese el ID del vuelo a eliminar: "))
            model.eliminar_ruta_menos_transitada(session, aerolinea, id_vuelo)
        elif option == 6:
            id_vuelo = uuid.UUID(input('Ingrese el ID del vuelo para la promoción: '))
            descuento = float(input('Ingrese el porcentaje de descuento (como un número decimal): '))
            fecha_inicio = input('Ingrese la fecha de inicio de la promoción (formato AAAA-MM-DD): ')
            fecha_fin = input('Ingrese la fecha de fin de la promoción (formato AAAA-MM-DD): ')
            condiciones = input('Ingrese las condiciones de la promoción: ')
            model.agregar_promocion(session, id_vuelo, descuento, fecha_inicio, fecha_fin, condiciones)
        elif option == 7:
            model.listar_promociones(session)
        elif option == 8:
            id_promocion = uuid.UUID(input('Ingrese el ID de la promoción a eliminar: '))
            model.eliminar_promocion(session, id_promocion)
        elif option == 9:
            break

if __name__ == '__main__':
    main()