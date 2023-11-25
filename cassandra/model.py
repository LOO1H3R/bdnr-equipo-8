#!/usr/bin/env python3
import logging

# Set logger
log = logging.getLogger()


CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""

CREATE_PASSANGERS_TABLE = """
    CREATE TABLE IF NOT EXISTS PASSANGERS (
        age INT,
        reason TEXT,
        transit TEXT,
        wait INT ,
        PRIMARY KEY ((age))
    )
"""

CREATE_AIRPORTS_TABLE = """
    CREATE TABLE IF NOT EXISTS AIRPORTS (
        airline TEXT,
        location TEXT,
        transit TEXT,
        start_date DATE,
        connection BOOLEAN,
        PRIMARY KEY ((airline))
    )
"""

def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))


def create_schema(session):
    log.info("Creating model schema")
    session.execute(CREATE_PASSANGERS_TABLE)
    session.execute(CREATE_AIRPORTS_TABLE)


def get_user_accounts(session, username):
    log.info(f"Retrieving {username} accounts")
    stmt = session.prepare(SELECT_USER_ACCOUNTS)
    rows = session.execute(stmt, [username])
    for row in rows:
        print(f"=== Account: {row.account_number} ===")
        print(f"- Cash Balance: {row.cash_balance}")