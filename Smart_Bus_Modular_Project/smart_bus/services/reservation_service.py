"""Business logic: routes, bookings, cancellation, availability and reports."""
from smart_bus.data import get_initial_routes, SUPPORTED_CITIES
from smart_bus.models import Booking

class ReservationService:
    def __init__(self):
        self.routes = get_initial_routes()
        self.bookings = []
        self._issued_booking_ids = set()
        self._next_booking_number = 1001

    def get_route(self, route_id):
        route_id = (route_id or "").strip().upper()
        return next((route for route in self.routes if route.route_id == route_id), None)

    def search_routes(self, term):
        term = (term or "").strip().lower()
        if not term:
            return []
        exact = self.get_route(term)
        if exact:
            return [exact]
        return [
            route for route in self.routes
            if term in route.route_id.lower()
            or term in route.departure_city.lower()
            or term in route.destination_city.lower()
        ]

    def book_ticket(self, passenger_name, passenger_age, route_id, seats):
        if not passenger_name or not passenger_name.strip():
            raise ValueError("Passenger name cannot be empty.")
        if not isinstance(passenger_age, int) or passenger_age <= 0:
            raise ValueError("Passenger age must be a positive integer.")
        if not isinstance(seats, int) or seats <= 0:
            raise ValueError("Seat quantity must be a positive integer.")

        route = self.get_route(route_id)
        if route is None:
            raise ValueError("Route ID does not exist.")
        if seats > route.available_seats:
            raise ValueError(f"Only {route.available_seats} seat(s) are available.")

        booking_id = f"B{self._next_booking_number}"
        while booking_id in self._issued_booking_ids:
            self._next_booking_number += 1
            booking_id = f"B{self._next_booking_number}"
        self._next_booking_number += 1

        booking = Booking(
            booking_id=booking_id,
            passenger_name=passenger_name.strip(),
            passenger_age=passenger_age,
            route_id=route.route_id,
            seats=seats,
            total_fare=route.ticket_price * seats,
        )
        # Change state only after all validation has passed.
        self.bookings.append(booking)
        self._issued_booking_ids.add(booking_id)
        route.available_seats -= seats
        return booking

    def cancel_booking(self, booking_id):
        booking_id = (booking_id or "").strip().upper()
        booking = next((item for item in self.bookings if item.booking_id == booking_id), None)
        if booking is None:
            raise ValueError("Booking ID was not found.")
        if booking.status != "Confirmed":
            raise ValueError("This booking has already been cancelled.")

        route = self.get_route(booking.route_id)
        route.available_seats += booking.seats
        booking.status = "Cancelled"
        return booking

    def get_availability(self, available_only=False):
        if available_only:
            return [route for route in self.routes if route.available_seats > 0]
        return list(self.routes)

    def get_schedule(self):
        schedule = {}
        for city in SUPPORTED_CITIES:
            schedule[city] = [
                route for route in self.routes if route.departure_city == city
            ]
        return schedule

    def get_report(self):
        confirmed = [b for b in self.bookings if b.status == "Confirmed"]
        cancelled = [b for b in self.bookings if b.status == "Cancelled"]
        return {
            "total_bookings": len(self.bookings),
            "confirmed_bookings": len(confirmed),
            "cancelled_bookings": len(cancelled),
            "reserved_seats": sum(b.seats for b in confirmed),
            "confirmed_revenue": sum(b.total_fare for b in confirmed),
            "fully_booked_routes": sum(1 for r in self.routes if r.available_seats == 0),
        }

    def list_bookings(self):
        return list(self.bookings)
