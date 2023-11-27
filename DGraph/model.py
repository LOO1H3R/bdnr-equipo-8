#!/usr/bin/env python3
import datetime
import json
import pydgraph
import random

from random import choice, randint, randrange
from datetime import datetime, timedelta



airlines = ["American Airlines", "Delta Airlines", "Alaska", "Aeromexico", "Volaris", "United Airlines", "British Airways", "Air France", "Emirates", "Qatar Airways", "Singapore Airlines", "Korean Air", "Japan Airlines", "Turkish Airlines", "LATAM Airlines", "Air Canada", "Copa Airlines"]
airports = ["PDX", "GDL", "SJC", "LAX", "JFK", "ORD", "LHR", "CDG", "DXB", "DOH", "SIN", "ICN", "NRT", "IST", "SCL", "YYZ", "PTY"]
genders = ["male", "female", "unspecified", "undisclosed"]
reasons = ["On vacation/Pleasure", "Business/Work", "Back Home"]
stays = ["Hotel", "Short-term homestay", "Home", "Friend/Family"]
transits = ["Airport cab", "Car rental", "Mobility as a service", "Public Transportation", "Pickup", "Own car"]
connections = [True, False]

# Función para generar fechas aleatorias
def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    print(days_between_dates)
    random_number_of_days = randrange(days_between_dates)
    rand_date = start_date + timedelta(days=random_number_of_days)
    return rand_date

start_date = datetime(2023, 1, 1)
mid_date = datetime(2023, 6, 30)
end_date = datetime(2023, 12, 31)


def set_schema(client):
    schema = """
    type Airport {
        code
        location
        airport_name
    }
    type Flight {
        flight_code
        number_of_passengers
        airline
        season
        reason
        duration
        departure_airport
        arrival_airport
    }

    type Season {
        season_name
        start_date
        end_date
    }

    type airline {
        name
    }


    code : string @index(exact) .
    location : string @index(exact) .
    flight_code : string @index(exact) .
    number_of_passengers : int .
    airline : [uid] @reverse .
    season : [uid] @reverse .
    reason : string @index(exact) .
    duration : int .
    start_date : datetime .
    end_date : datetime .
    departure_airport : [uid] @reverse .
    arrival_airport : [uid] @reverse .
    season_name : string @index(exact) .
    name : string @index(exact) .
    airport_name : string @index(exact) .
    """
    return client.alter(pydgraph.Operation(schema=schema))


def create_data(client):
    # Create a new transaction.
    txn = client.txn()
    try:
        data = []
        for _ in range(100):
            departure_airport = choice(airports)
            arrival_airport = choice(airports)
            while departure_airport == arrival_airport:
                arrival_airport = choice(airports)
            print(_)
            start_date = random_date(datetime(2023, 1, 1), datetime(2023, 10, 30))
            end_date = random_date(datetime(2023, 11, 30), datetime(2024, 2, 28))
            airline = choice(airlines)
            season_name = "Spring" if (start_date.month < 6 and start_date.month > 2) else "Summer" if start_date.month < 9 else "Fall" if start_date.month < 11 else "Winter" if (start_date.month > 11 and start_date.month < 1) else "Spring"
            flight_data = {
                "flight_code": "{}-{}".format(choice(airlines), randint(1000, 9999)),
                "airline": {
                    "uid": "_:{}".format(airline),
                    "name": airline
                },
                "season": {
                    "uid": "_:{}".format(season_name),
                    "season_name": season_name,
                    "start_date": start_date.isoformat(),
                    "end_date": start_date.isoformat()
                },
                "number_of_passengers": randint(1, 500),
                "reason": choice(reasons),
                "duration": randint(0, 72), # Duración en horas
                "departure_airport": {
                    "uid": "_:+{}".format(departure_airport),
                    "code": departure_airport,
                    "airport_name": departure_airport
                },
                "arrival_airport": {
                    "uid": "_:+{}".format(arrival_airport),
                    "code": arrival_airport,
                    "airport_name": arrival_airport
                }
            }

            data.append(flight_data)

        


        response = txn.mutate(set_obj=data)

        # Commit transaction.
        commit_response = txn.commit()
        print(f"Commit Response: {commit_response}")

        print(f"UIDs: {response.uids}")
    finally:
        # Clean up. 
        # Calling this after txn.commit() is a no-op and hence safe.
        txn.discard()


def delete_person(client, name):
    # Create a new transaction.
    txn = client.txn()
    try:
        query1 = """query search_person($a: string) {
            all(func: eq(name, $a)) {
               uid
            }
        }"""
        variables1 = {'$a': name}
        res1 = client.txn(read_only=True).query(query1, variables=variables1)
        ppl1 = json.loads(res1.json)
        for person in ppl1['all']:
            print("UID: " + person['uid'])
            txn.mutate(del_obj=person)
            print(f"{name} deleted")
        commit_response = txn.commit()
        print(commit_response)
    finally:
        txn.discard()


def search_person(client, name):
    query = """query search_person($a: string) {
        all(func: eq(name, $a)) {
            uid
            name
            age
            married
            loc
            dob
            friend {
                name
                age
            }
            school {
                name
            }
        }
    }"""

    variables = {'$a': name}
    res = client.txn(read_only=True).query(query, variables=variables)
    ppl = json.loads(res.json)

    # Print results.
    print(f"Number of people named {name}: {len(ppl['all'])}")
    print(f"Data associated with {name}:\n{json.dumps(ppl, indent=2)}")

def number_of_flights(client, airport):
    print(airport)
    query = """query number_of_flights($a: string) {
        airport(func: eq(code, $a)) {
            uid
            code
            location
            airport_name
            numFlights: count(~arrival_airport)
            }
    }"""

    variables = {'$a': airport}
    res = client.txn(read_only=True).query(query, variables=variables)
    aiport = json.loads(res.json)
    print(aiport)
    # Print results.
    print(f"Number of flights for {airport}: {aiport['airport'][0]['numFlights']}")
    print(f"Data associated with {airport}:\n{json.dumps(aiport, indent=2)}")
    

def most_visited_season(client, airport):
    query = """query most_visited_season($a: string) {
  airport(func: eq(airport_name, "CDG")) {
    uid
    airport_name
    flights as ~arrival_airport {
      uid
      arrival_airport
    }
  }

  seasonWithMostFlights(func: uid(flights)) {
    uid
    season_name
    flight_code
    season{
			season_name
    }
  }
}
"""

    variables = {'$a': airport}
    res = client.txn(read_only=True).query(query, variables=variables)
    aiport = json.loads(res.json)
    #print(aiport)
    # Print results.
    spring = 0
    summer = 0
    fall = 0
    winter = 0
    for i in range(len(aiport['seasonWithMostFlights'])):
        print(f"Airport flight {airport}: {aiport['seasonWithMostFlights'][i]['flight_code'], aiport['seasonWithMostFlights'][i]['season'][0]['season_name']}")
        if aiport['seasonWithMostFlights'][i]['season'][0]['season_name'] == "Spring":
            spring += 1
        elif aiport['seasonWithMostFlights'][i]['season'][0]['season_name'] == "Summer":
            summer += 1
        elif aiport['seasonWithMostFlights'][i]['season'][0]['season_name'] == "Fall":
            fall += 1
        elif aiport['seasonWithMostFlights'][i]['season'][0]['season_name'] == "Winter":
            winter += 1
    print(f"Most visited season for {airport}:"+(" Spring" if spring > summer and spring > fall and spring > winter else " Summer" if summer > spring and summer > fall and summer > winter else " Fall" if fall > spring and fall > summer and fall > winter else " Winter"))

def most_visited_reason(client, airport):
    query = """query most_visited_reason($a: string) {
  airport(func: eq(airport_name, "CDG")) {
    uid
    airport_name
    flights as ~arrival_airport {
      uid
      arrival_airport
    }
  }

  reasonWithMostFlights(func: uid(flights)) {
    uid
    reason
    flight_code
  }
}
"""

    variables = {'$a': airport}
    res = client.txn(read_only=True).query(query, variables=variables)
    aiport = json.loads(res.json)
    #print(aiport)
    # Print results.
    vacation = 0
    business = 0
    home = 0
    for i in range(len(aiport['reasonWithMostFlights'])):
        print(f"Airport flight {airport}: {aiport['reasonWithMostFlights'][i]['flight_code'], aiport['reasonWithMostFlights'][i]['reason']}")
        if aiport['reasonWithMostFlights'][i]['reason'] == "On vacation/Pleasure":
            vacation += 1
        elif aiport['reasonWithMostFlights'][i]['reason'] == "Business/Work":
            business += 1
        elif aiport['reasonWithMostFlights'][i]['reason'] == "Back Home":
            home += 1
    print(f"Most visited reason for {airport}:"+(" Vacation" if vacation > business and vacation > home else " Business" if business > vacation and business > home else " Home"))

def season_with_most_flights(client):
    query = """{
        topSeason(func: has(start_date)) {
            uid
            season_name
            start_date
            end_date
            numFlights: count(~season)
        }
        }
        """
    
    res = client.txn(read_only=True).query(query)
    season = json.loads(res.json)
    #print(season)
    # Print results.
    print(f"Season with most flights:"+(" Spring" if season['topSeason'][0]['season_name'] == "Spring" else " Summer" if season['topSeason'][0]['season_name'] == "Summer" else " Fall" if season['topSeason'][0]['season_name'] == "Fall" else " Winter"))

    
def drop_all(client):
    return client.alter(pydgraph.Operation(drop_all=True))
