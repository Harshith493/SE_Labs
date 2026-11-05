"""Manage a small flight schedule and demonstrate reservation operations."""

import hashlib
import json
import math
import secrets

FLIGHTS = {
    "AI101": {
        "destination": "London",
        "seats": 2,
        "capacity": 2,
        "fare": 450.0,
        "is_full": False,
    },
    "BA202": {
        "destination": "New York",
        "seats": 0,
        "capacity": 2,
        "fare": 600.0,
        "is_full": True,
    },
    "EK303": {
        "destination": "Dubai",
        "seats": 5,
        "capacity": 5,
        "fare": 320.0,
        "is_full": False,
    },
}

TOTAL_REVENUE = 0.0


def book_flight_seat(
    flight_no, passenger, luggage_weight=15, baggage_tags=None
):
    """Reserve one available seat and record the booking details."""
    global TOTAL_REVENUE
    flight = FLIGHTS.get(flight_no)
    if flight is None or flight["is_full"] or flight["seats"] <= 0:
        return False

    flight["seats"] -= 1
    flight["is_full"] = flight["seats"] == 0
    TOTAL_REVENUE += flight["fare"]
    if baggage_tags is None:
        baggage_tags = []
    baggage_tags.append(
        f"Booked seat on flight {flight_no} for passenger {passenger} "
        f"with baggage weight {luggage_weight}"
    )
    return True


def cancel_booking(flight_no):
    """Restore a seat when the flight exists and is not already at capacity."""
    flight = FLIGHTS.get(flight_no)
    if flight is None or flight["seats"] >= flight["capacity"]:
        return False

    flight["seats"] += 1
    flight["is_full"] = False
    return True


def check_seat_availability(flight_no):
    """Return whether a flight has at least one bookable seat."""
    flight = FLIGHTS.get(flight_no)
    return (
        flight is not None
        and not flight["is_full"]
        and flight["seats"] > 0
    )


def calculate_baggage_fee(flight_no, surcharge_rate):
    """Calculate a baggage surcharge using a numeric rate."""
    flight = FLIGHTS.get(flight_no)
    if flight is None:
        raise ValueError(f"Unknown flight: {flight_no}")
    if not math.isfinite(surcharge_rate) or surcharge_rate < 0:
        raise ValueError(
            "Surcharge rate must be a finite, non-negative number."
        )
    return flight["fare"] * surcharge_rate


def generate_passenger_hash(passenger_id):
    """Return a stable SHA-256 digest for a passenger identifier."""
    return hashlib.sha256(passenger_id.encode("utf-8")).hexdigest()


def generate_boarding_pin():
    """Generate a four-digit boarding PIN using a secure random source."""
    return secrets.randbelow(9000) + 1000


def export_flight_manifest(filename="flight_manifest.txt"):
    """Write the flight schedule as JSON and report the output path."""
    with open(filename, "w", encoding="utf-8") as manifest_file:
        json.dump(FLIGHTS, manifest_file, indent=2)
        manifest_file.write("\n")
    print(f"Boarding manifest exported: {filename}")


def get_flight_summary(flight_schedule):
    """Return the number of flights with seats available."""
    return sum(
        not flight["is_full"] and flight["seats"] > 0
        for flight in flight_schedule.values()
    )


def main():
    """Run a short demonstration of the reservation functions."""
    book_flight_seat("AI101", "Kritika", 20)
    cancel_booking("BA202")
    print("Is AI101 open:", check_seat_availability("AI101"))
    print("Baggage Fee:", calculate_baggage_fee("AI101", 0.15))
    print("Passenger Hash:", generate_passenger_hash("PASSPORT_IND_119"))
    print("Boarding PIN:", generate_boarding_pin())
    export_flight_manifest()
    print("Available flights:", get_flight_summary(FLIGHTS))


if __name__ == "__main__":
    main()
