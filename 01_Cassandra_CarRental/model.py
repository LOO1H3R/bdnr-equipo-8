#!/usr/bin/env python3
import logging

# Set logger
log = logging.getLogger()


CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""

CREATE_PASSANGERS_TABLE = """
    CREATE TABLE IF NOT EXISTS passangers (
        airline TEXT,
        age INT,
        reason TEXT,
        transit TEXT,
        wait INT,
        PRIMARY KEY (airline)
    ) ;
"""

CREATE_AIRPORTS_TABLE = """
    CREATE TABLE IF NOT EXISTS AIRPORTS (
        airline TEXT,
        location TEXT,
        transit TEXT,
        start_date timestamp,
        connection BOOLEAN,
        PRIMARY KEY ((transit))
    )
"""

CREATE_PASSANGERS_TABLE_BY_REASON = """
    CREATE TABLE IF NOT EXISTS PASSANGERS_BY_REASON (
        airline TEXT,
        age INT,
        reason TEXT,
        transit TEXT,
        wait INT,
        PRIMARY KEY (reason)
    ) ;

"""

CREATE_PASSANGER_BY_TRANSIT = """
    CREATE TABLE IF NOT EXISTS PASSANGERS_BY_TRANSIT (
        airline TEXT,
        location TEXT,
        transit TEXT,
        start_date timestamp,
        connection BOOLEAN,
        PRIMARY KEY (transit)
    )
"""



SELECT_PASSANGERS_OLDER_THAN = """
SELECT airline, age FROM passangers WHERE age > ? ALLOW FILTERING;
"""

SELECT_PASSANGERS_BY_REASON = """
SELECT airline, reason, COUNT(*) as passenger_count FROM PASSANGERS_BY_REASON WHERE reason = ?;
"""

SELECT_AIRPORTS_BY_TRANSIT = """
SELECT airline, transit FROM airports WHERE transit = ?;
"""

SELECT_AIRPORTS_BY_WAIT = """
SELECT airline, wait FROM airports WHERE wait > ? ;
"""

def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))


def create_schema(session):
    log.info("Creating model schema")
    session.execute(CREATE_PASSANGERS_TABLE)
    session.execute(CREATE_AIRPORTS_TABLE)
    session.execute(CREATE_PASSANGERS_TABLE_BY_REASON)
    session.execute(CREATE_PASSANGER_BY_TRANSIT)


def get_passangers_older_than(session, age):
    log.info(f"Getting passangers older than {age}")
    stmt = session.prepare(SELECT_PASSANGERS_OLDER_THAN)
    rows =    session.execute(stmt, {age})
    print(f"Airline\t\t\tAge")
    for row in rows:
        print(f"{row.airline}\t\t\t{row.age}")

def get_passangers_by_reason(session, reason):
    log.info(f"Getting passangers by reason {reason}")
    stmt = session.prepare(SELECT_PASSANGERS_BY_REASON)
    rows = session.execute(stmt, {reason})
    print(f"Airline\t\t\tReason")
    for row in rows:
        print(f"{row.airline}\t\t\t{row.reason}")

def get_airports_by_transit(session, transit):
    log.info(f"Getting airports by transit {transit}")
    stmt = session.prepare(SELECT_AIRPORTS_BY_TRANSIT)
    rows = session.execute(stmt, {transit})
    print(f"Airline\t\t\tPassenger Count")
    for row in rows:
        print(f"{row.airline}\t\t\t{row.passenger_count}")

def get_airports_by_wait(session, wait):
    log.info(f"Getting airports by wait {wait}")
    stmt = session.prepare(SELECT_AIRPORTS_BY_WAIT)
    rows = session.execute(stmt, {wait})
    print(f"Airline\t\t\tPassenger Count")
    for row in rows:
        print(f"{row.airline}\t\t\t{row.passenger_count}")

