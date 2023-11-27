#!/usr/bin/env python3
import os

import pydgraph

import model

DGRAPH_URI = os.getenv('DGRAPH_URI', 'localhost:9080')



def print_menu():
    mm_options = {
        1: "Create data",
        2: "Number of flights for a specific airport",
        3: "Most visited season for a specific airport",
        4: "Most visited reason for a specific airport",
        5: "Season with most flights",
        7: "Drop All",
        8: "Exit",
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])


def create_client_stub():
    return pydgraph.DgraphClientStub(DGRAPH_URI)


def create_client(client_stub):
    return pydgraph.DgraphClient(client_stub)


def close_client_stub(client_stub):
    client_stub.close()


def main():
    # Init Client Stub and Dgraph Client
    client_stub = create_client_stub()
    client = create_client(client_stub)

    # Create schema
    model.set_schema(client)

    while(True):
        print_menu()
        option = int(input('Enter your choice: '))
        if option == 1:
            model.create_data(client)
        if option == 2:
            airport = input("Name: ")
            model.number_of_flights(client, airport)
        if option == 3:
            airport = input("Name: ")
            model.most_visited_season(client, airport)
        if option == 4:
            airport = input("Name: ")
            model.most_visited_reason(client, airport)
        if option == 5:
            model.season_with_most_flights(client)
        if option == 7:
            model.drop_all(client)
        if option == 8:
            model.drop_all(client)
            close_client_stub(client_stub)
            exit(0)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Error: {}'.format(e))