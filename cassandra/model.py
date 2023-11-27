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
        PRIMARY KEY (airline, age)
    ) WITH CLUSTERING ORDER BY (age ASC);
"""

CREATE_AIRPORTS_TABLE = """
    CREATE TABLE IF NOT EXISTS AIRPORTS (
        airline TEXT,
        location TEXT,
        transit TEXT,
        start_date timestamp,
        connection BOOLEAN,
        PRIMARY KEY ((airline))
    )
"""

CREATE_PASSANGERS_TABLE_BY_REASON = """
    CREATE TABLE IF NOT EXISTS passangers_by_reason (
        airline TEXT,
        age INT,
        reason TEXT,
        transit TEXT,
        wait INT,
        PRIMARY KEY (reason, airline)
    ) WITH CLUSTERING ORDER BY (airline ASC);

"""

SELECT_PASSANGERS_OLDER_THAN = """
    SELECT airline FROM PASSANGERS WHERE age > ?;
"""
#TODO: ORDER BY NUMBER OF PASSANGERS
SELECT_PASSANGERS_BY_REASON = """
    SELECT airline, reason FROM PASSANGERS_BY_REASON WHERE reason = ?;
"""


def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))


def create_schema(session):
    log.info("Creating model schema")
    session.execute(CREATE_PASSANGERS_TABLE)
    session.execute(CREATE_AIRPORTS_TABLE)
    session.execute(CREATE_PASSANGERS_TABLE_BY_REASON)


def get_passangers_older_than(session, age):
    log.info(f"Getting passangers older than {age}")
    stmt = session.prepare(SELECT_PASSANGERS_OLDER_THAN)
    session.execute(stmt, {age})

def get_passangers_by_reason(session, reason):
    log.info(f"Getting passangers by reason {reason}")
    stmt = session.prepare(SELECT_PASSANGERS_BY_REASON)
    rows = session.execute(stmt, {reason})
    print(f"Airline\t\t\tReason")
    for row in rows:
        print(f"{row.airline}\t{row.reason}")

