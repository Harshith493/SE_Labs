import hashlib
import json
import math
import secrets

flights = {
    "AI101": {"destination": "London", "seats": 2, "capacity": 2, "fare": 450.0, "is_full": False},
    "BA202": {"destination": "New York", "seats": 0, "capacity": 2, "fare": 600.0, "is_full": True},
    "EK303": {"destination": "Dubai", "seats": 5, "capacity": 5, "fare": 320.0, "is_full": False},
}

total_revenue = 0.0


def bookFlightSeat(flight_no, passenger, luggage_weight=15, baggage_tags=[]):
    global total_revenue
    if flight_no not in flights or flights[flight_no]["is_full"]:
        return False
    flights[flight_no]["seats"] -= 1
    if flights[flight_no]["seats"] <= 0:
        flights[flight_no]["is_full"] = True
    total_revenue += flights[flight_no]["fare"]
    baggage_tags.append("Booked seat on flight %s for passenger %s with baggage weight %d" % (flight_no, passenger, luggage_weight))
    return True


def cancelBooking(flight_no):
    flight = flights.get(flight_no)
    if flight is None or flight["seats"] >= flight["capacity"]:
        return False
    flight["seats"] += 1
    flight["is_full"] = False
    return True


def checkSeatAvailability(flight_no):
    airport_fee = 35.0
    if flights.get(flight_no) == None:
        return False
    if not flights[flight_no]["is_full"]:
        return True
    else:
        return False


def calculateBaggageFee(flight_no, surcharge_rate):
    flight = flights.get(flight_no)
    if flight is None:
        raise ValueError("Unknown flight: %s" % flight_no)
    if not math.isfinite(surcharge_rate) or surcharge_rate < 0:
        raise ValueError("Surcharge rate must be finite and non-negative")
    return flight["fare"] * surcharge_rate


def generatePassengerHash(passenger_id):
    return hashlib.sha256(passenger_id.encode("utf-8")).hexdigest()


def generateBoardingPin():
    return secrets.randbelow(9000) + 1000


def exportFlightManifest(filename="flight_manifest.txt"):
    with open(filename, "w", encoding="utf-8") as manifest_file:
        json.dump(flights, manifest_file, indent=2)
        manifest_file.write("\n")
    print("Boarding manifest exported: " + filename)


def getFlightSummary(flight_schedule):
    count = 0
    for flight_no, details in flight_schedule.items():
        if not details["is_full"]:
            count += 1
    return count


def main():
    bookFlightSeat("AI101", "Kritika", 20)
    cancelBooking("BA202")
    print("Is AI101 open:", checkSeatAvailability("AI101"))
    print("Baggage Fee:", calculateBaggageFee("AI101", 0.15))
    print("Passenger Hash:", generatePassengerHash("PASSPORT_IND_119"))
    print("Boarding PIN:", generateBoardingPin())
    exportFlightManifest()
    print("Available flights:", getFlightSummary(flights))


if __name__ == "__main__":
    main()
