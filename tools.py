from typing import List
from langchain.tools import tool

@tool
def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: str = "",
    max_price: float = 0.0,
) -> List[dict]:
    """Search for flights between two cities on given dates."""
    return [
        {
            "offer_id": "FLIGHT_OFFER_DEMO_1",
            "airline": "Demo Air",
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "price": 550.0,
            "duration_hours": 12,
        }
    ]

@tool
def book_flight(offer_id: str) -> str:
    """Book a flight given an offer ID (stub)."""
    return f"Flight booked successfully with offer_id={offer_id}"

@tool
def search_hotels(
    city: str,
    checkin_date: str,
    checkout_date: str,
    max_price_per_night: float = 0.0,
    area_preference: str = ""
) -> List[dict]:
    """Search for hotels in a city between given dates."""
    return [
        {
            "name": "Demo Hotel Shinjuku",
            "city": city,
            "price_per_night": 120.0,
            "area": "Shinjuku",
            "rating": 4.4,
        }
    ]

@tool
def book_hotel(hotel_name: str, checkin_date: str, checkout_date: str) -> str:
    """Book a hotel by name and dates (stub)."""
    return f"Hotel '{hotel_name}' booked from {checkin_date} to {checkout_date}"

@tool
def estimate_trip_cost(
    flight_price: float,
    hotel_price_per_night: float,
    nights: int,
    extra_budget: float = 0.0
) -> float:
    """Estimate total trip cost."""
    return flight_price + hotel_price_per_night * nights + extra_budget