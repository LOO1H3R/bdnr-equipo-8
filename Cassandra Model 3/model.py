#!/usr/bin/env python3
import logging
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import uuid

# Configuración del logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('rutas_promocionales.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Consultas CQL tipo CREATE
CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""

CREATE_PROMOCIONES_RUTAS = """
CREATE TABLE IF NOT EXISTS promociones_rutas (
    id_promocion UUID PRIMARY KEY,
    id_vuelo UUID,
    descuento DECIMAL,
    fecha_inicio DATE,
    fecha_fin DATE,
    condiciones TEXT
)
"""

CREATE_DATOS_PASAJEROS = """
    CREATE TABLE IF NOT EXISTS datos_pasajero_vuelo (
        aerolinea TEXT,
        id_vuelo UUID,
        desde TEXT,
        hacia TEXT,
        capacidad INT,
        recuento_pasajeros INT,
        PRIMARY KEY ((aerolinea), id_vuelo)
    )
"""

CREATE_RUTAS_MENOS_TRANSITADAS = """
    CREATE TABLE IF NOT EXISTS rutas_menos_transitadas (
        aerolinea TEXT,
        id_vuelo UUID,
        desde TEXT,
        hacia TEXT,
        capacidad INT,
        recuento_pasajeros INT,
        PRIMARY KEY ((aerolinea), id_vuelo)
    )
"""

# Consultas CQL tipo select
CONTAR_PASAJERON_POR_VUELO = """
    SELECT COUNT(*) FROM datos_pasajero_vuelo 
    WHERE from_airport = ? AND to_airport = ? AND day = ? AND month = ? AND year = ?
"""

SELECT_RUTAS_AEROLINEA = """
    SELECT * FROM datos_pasajero_vuelo WHERE aerolinea = ?
"""

SELECT_RUTAS_PASAJEROS = """
    SELECT * FROM datos_pasajero_vuelo WHERE recuento_pasajeros <= ?
    ALLOW FILTERING
"""


# Función para crear un keyspace, en caso de ser necesario.
def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))

# Función para ejecutar los CREATE's y generar las tablas y sus atributos.
def create_schema(session):
    log.info("Creating model schema")
    session.execute(CREATE_RUTAS_MENOS_TRANSITADAS)
    session.execute(CREATE_DATOS_PASAJEROS)
    session.execute(CREATE_PROMOCIONES_RUTAS)
    
# Función para formatear la salida de datos.
def format_row(row):
    return f"Aerolínea: {row.aerolinea}, Vuelo ID: {row.id_vuelo}, Desde: {row.desde}, Hacia: {row.hacia}, Capacidad: {row.capacidad}, Pasajeros: {row.recuento_pasajeros}"


# 1.- Función para crear tabla con las rutas menos transitadas a partir de un número N establecido por el usuario
def generar_commando_insert_cql_datos_filtrados(csv_file, cql_file, max_passengers):
    try:
        with open(csv_file, newline='') as csvfile, open(cql_file, 'w') as cqlfile:
            reader = csv.DictReader(csvfile)
            passenger_counts = {}

            for row in reader:
                flight_key = (row['airline'], row['from'], row['to'])
                passenger_counts[flight_key] = passenger_counts.get(flight_key, 0) + 1

            for flight_key, count in passenger_counts.items():
                if count <= max_passengers:
                    aerolinea, desde, hacia = flight_key
                    id_vuelo = uuid.uuid4()
                    capacidad = 100
                    cqlfile.write(f"INSERT INTO rutas_menos_transitadas (id_vuelo, aerolinea, desde, hacia, capacidad, recuento_pasajeros) VALUES ({id_vuelo}, '{aerolinea}', '{desde}', '{hacia}', {capacidad}, {count});\n")

        logging.info("Archivo CQL generado con éxito.")
    except Exception as e:
        logging.error(f"Error al generar el archivo CQL: {e}")

# 2.- Función para obtener todas las rutas menos transitadas de una aerolínea específica.
def agregar_ruta_menos_transitada(session, aerolinea, id_vuelo, desde, hacia, capacidad, recuento_pasajeros):
    try:
        session.execute(
            """
            INSERT INTO datos_pasajero_vuelo (aerolinea, id_vuelo, desde, hacia, capacidad, recuento_pasajeros)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (aerolinea, id_vuelo, desde, hacia, capacidad, recuento_pasajeros)
        )
        session.execute(
            """
            INSERT INTO rutas_menos_transitadas (aerolinea, id_vuelo, desde, hacia, capacidad, recuento_pasajeros)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (aerolinea, id_vuelo, desde, hacia, capacidad, recuento_pasajeros)
        )

        log.info("Ruta menos transitada agregada en ambas tablas")
    except Exception as e:
        log.error(f"Error al agregar ruta: {e}")

# 3.- Función para buscar a los vuelos con menos pasajeros
def consultar_rutas_con_menos_pasajeros(session, max_pasajeros):
    try:
        rows = session.execute(
            "SELECT * FROM rutas_menos_transitadas WHERE recuento_pasajeros <= %s ALLOW FILTERING",
            (max_pasajeros,)
        )
        for row in rows:
            print(format_row(row))
    except Exception as e:
        log.error(f"Error al consultar vuelos: {e}")

# 4.- Función para obtener todas las rutas menos transitadas de una aerolínea específica.
def get_rutas_menos_transitadas_aerolinea(session, aerolinea):
    try:
        if not aerolinea:
            raise ValueError("El nombre de la aerolínea no puede estar vacío")

        # Update passenger count before retrieving routes
        update_passenger_count(session)

        log.info(f"Retrieving routes for airline {aerolinea}")
        stmt = session.prepare(SELECT_RUTAS_AEROLINEA)
        rows = session.execute(stmt, [aerolinea])
        for row in rows:
            print(format_row(row))
        return True  
    except Exception as e:
        log.error(f"Error while consulting routes: {e}")
        return False

# Función para obtener rutas con N número de pasajeros o menos
def get_rutas_por_pasajeros_aerolinea(session, aerolinea, max_pasajeros):
    try:
        if max_pasajeros <= 0:
            raise ValueError("El número máximo de pasajeros debe ser mayor que 0")

        log.info(f"Retrieving routes with {max_pasajeros} passengers or less for airline {aerolinea}")
        stmt = session.prepare("SELECT * FROM rutas_menos_transitadas WHERE aerolinea = ? AND recuento_pasajeros <= ? ALLOW FILTERING")
        rows = session.execute(stmt, [aerolinea, max_pasajeros])
        for row in rows:
            print(format_row(row))
        return True
    except Exception as e:
        log.error(f"Error while consulting routes: {e}")
        return False

# 5.- Función para eliminar una de las rutas menos transitadas
def eliminar_ruta_menos_transitada(session, aerolinea, id_vuelo):
    try:
        session.execute(
            "DELETE FROM rutas_menos_transitadas WHERE aerolinea = %s AND id_vuelo = %s",
            (aerolinea, id_vuelo)
        )
        log.info("Ruta menos transitada eliminada")
    except Exception as e:
        log.error(f"Error al eliminar ruta: {e}")

# 6.- Función para agregar una promoción
def agregar_promocion(session, id_vuelo, descuento, fecha_inicio, fecha_fin, condiciones):
    id_promocion = uuid.uuid4()
    session.execute(
        """
        INSERT INTO promociones_rutas (id_promocion, id_vuelo, descuento, fecha_inicio, fecha_fin, condiciones)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (id_promocion, id_vuelo, descuento, fecha_inicio, fecha_fin, condiciones)
    )
    log.info(f"Promoción agregada: {id_promocion}")

# 7.- Función para listar promociones
def listar_promociones(session):
    promociones = session.execute("SELECT * FROM promociones_rutas")
    for promocion in promociones:
        print(promocion)

# 8.- Función para eliminar una promoción
def eliminar_promocion(session, id_promocion):
    session.execute(
        "DELETE FROM promociones_rutas WHERE id_promocion = %s",
        (id_promocion,)
    )
    log.info(f"Promoción eliminada: {id_promocion}")
