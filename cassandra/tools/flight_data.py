#!/usr/bin/env python3
import datetime
import random
import uuid


CQL_FILE = 'data.cql'


from random import choice, randint, randrange


airlines = ["American Airlines", "Delta Airlines", "Alaska", "Aeromexico", "Volaris", "United Airlines", "British Airways", "Air France", "Emirates", "Qatar Airways", "Singapore Airlines", "Korean Air", "Japan Airlines", "Turkish Airlines", "LATAM Airlines", "Air Canada", "Copa Airlines"]                                                                                       
airports = ["PDX", "GDL", "SJC", "LAX", "JFK", "ORD", "LHR", "CDG", "DXB", "DOH", "SIN", "ICN", "NRT", "IST", "SCL", "YYZ", "PTY"]
genders = ["male", "female", "unspecified", "undisclosed"]
reasons = ["On vacation/Pleasure", "Business/Work", "Back Home"]
stays = ["Hotel", "Short-term homestay", "Home", "Friend/Family"]
transits = ["Airport cab", "Car rental", "Mobility as a service", "Public Transportation", "Pickup", "Own car"]
connections = [True, False]


def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = randrange(days_between_dates)
    rand_date = start_date + datetime.timedelta(days=random_number_of_days)
    return rand_date




def cql_stmt_generator(accounts_num=5000, positions_by_account=100, trades_by_account=1000):
    passangers_stmt = "INSERT INTO PASSANGERS(age, reason, transit, wait) VALUES ({}, '{}', '{}', {});"
    airports_stmt = "INSERT INTO AIRPORTS(airline, location, transit, start_date, connection) VALUES ('{}', '{}', '{}', '{}', {});"

    with open(CQL_FILE, "w") as fd:
        for i in range(accounts_num):
            from_airport = random.choice(airports)
            to_airport = random.choice(airports)
            while from_airport == to_airport:
                to_airport = choice(airports)
            date = random_date(datetime.datetime(2013, 1, 1), datetime.datetime(2023, 4, 25))
            date_object = datetime.strptime(date_string, "%Y-%m-%d")
            timestamp_seconds = int(date_object.timestamp())
            reason = choice(reasons)
            stay = choice(stays)
            connection = choice(connections)
            wait = randint(30, 720)
            transit = choice(transits)
            airline = choice(airlines)
            gender = choice(genders)
            age = randint(1,90)
            if not connection:
                wait = 0
            else:
                transit = ""
            if reason == "Back Home":
                stay = "Home"
                connection = False
                wait = 0
            fd.write(passangers_stmt.format(age, reason, transit, wait))
            fd.write('\n')
            fd.write(airports_stmt.format(airline, from_airport, transit, timestamp, connection))
            fd.write('\n')




def main():
    cql_stmt_generator()


if __name__ == "__main__":
    main()