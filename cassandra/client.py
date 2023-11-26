#!/usr/bin/env python3
import logging
import os
import random

from cassandra.cluster import Cluster

import model

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('flights.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars releated to Cassandra App
CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'investments')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')


def print_menu():
    mm_options = {
        1: 'show all passangers older than 18 years old',
        2: 'show all passangers which flight reason is "Business/Work"',
        3: 'show all passangers which flight reason is "On vacation/Pleasure"',
        4: 'show all airports which transits are "Car rental"',
        5: 'show all airports which wait is greater than 1 hour',
        6: 'show all airports which have more reason "Business/Work"',
        7: 'exit'
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])


def print_trade_history_menu():
    thm_options = {
        1: 'show all passangers older than 18 years old',
        2: 'show all passangers which flight reason is "Business/Work"',
        3: 'show all passangers which flight reason is "On vacation/Pleasure"',
        4: 'show all airports which transits are "Car rental"',
        5: 'show all airports which wait is greater than 1 hour',
        6: 'show all airports which have more reason "Business/Work"',
        7: 'exit'
    }
    for key in thm_options.keys():
        print('    ', key, '--', thm_options[key])


def set_username():
    username = input('**** Username to use app: ')
    log.info(f"Username set to {username}")
    return username


def get_instrument_value(instrument):
    instr_mock_sum = sum(bytearray(instrument, encoding='utf-8'))
    return random.uniform(1.0, instr_mock_sum)


def main():
    log.info("Connecting to Cluster")
    cluster = Cluster(CLUSTER_IPS.split(','))
    session = cluster.connect()

    model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)

    model.create_schema(session)

    username = set_username()

    while(True):
        print_menu()
        option = int(input('Enter your choice: '))
        if option == 1:
            model.get_passangers_older_than(session, 18)
        elif option == 2:
            model.get_passangers_by_reason(session, 'Business/Work')
        elif option == 3:
            model.get_passangers_by_reason(session, 'On vacation/Pleasure')
        elif option == 4:
            model.get_airports_by_transit(session, 'Car rental')
        elif option == 5:
            model.get_airports_by_wait(session, 60)
        elif option == 6:
            model.get_passangers_by_reason(session, 'Business/Work')
        elif option == 7:
            exit(0)


if __name__ == '__main__':
    main()
