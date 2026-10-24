"""Typed data models for routes and bookings."""
from dataclasses import dataclass, asdict

@dataclass
class Route:
    route_id: str
    departure_city: str
    destination_city: str
    departure_time: str
    ticket_price: int
    total_seats: int
    available_seats: int

    def to_dict(self):
        return asdict(self)

@dataclass
class Booking:
    booking_id: str
    passenger_name: str
    passenger_age: int
    route_id: str
    seats: int
    total_fare: int
    status: str = "Confirmed"

    def to_dict(self):
        return asdict(self)
