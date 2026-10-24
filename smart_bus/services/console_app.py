"""Text-console user interface. Keeps input/output out of business logic."""
from smart_bus.services.reservation_service import ReservationService

def _read_int(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Please enter a valid whole number.")
        return None

def _print_route(route):
    status = "Fully Booked" if route.available_seats == 0 else (
        "Available" if route.available_seats == route.total_seats else "Partially Booked"
    )
    print(f"{route.route_id} | {route.departure_city} -> {route.destination_city} | "
          f"{route.departure_time} | Rs. {route.ticket_price:,} | "
          f"{route.available_seats}/{route.total_seats} seats | {status}")

def run_console():
    service = ReservationService()
    while True:
        print("""
========== SMART BUS RESERVATION SYSTEM ==========
1. View Routes
2. Search Routes
3. Book Ticket
4. View Bookings
5. Cancel Booking
6. Seat Availability
7. Booking Report
8. Route Schedule
9. Exit
==================================================
""")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            for index, route in enumerate(service.routes, 1):
                print(f"{index}. ", end="")
                _print_route(route)
        elif choice == "2":
            matches = service.search_routes(input("Route ID or city: "))
            if matches:
                for route in matches:
                    _print_route(route)
            else:
                print("No matching routes found.")
        elif choice == "3":
            name = input("Passenger name: ").strip()
            age = _read_int("Passenger age: ")
            route_id = input("Route ID: ").strip()
            seats = _read_int("Number of seats: ")
            if age is None or seats is None:
                continue
            try:
                booking = service.book_ticket(name, age, route_id, seats)
                print(f"Booking confirmed: {booking.booking_id} | "
                      f"{booking.passenger_name} | {booking.seats} seat(s) | "
                      f"Rs. {booking.total_fare:,}")
            except ValueError as exc:
                print(f"Booking failed: {exc}")
        elif choice == "4":
            bookings = service.list_bookings()
            if not bookings:
                print("No bookings found.")
            for index, booking in enumerate(bookings, 1):
                print(f"{index}. {booking.booking_id} | {booking.passenger_name} | "
                      f"{booking.route_id} | {booking.seats} seat(s) | "
                      f"Rs. {booking.total_fare:,} | {booking.status}")
        elif choice == "5":
            try:
                booking = service.cancel_booking(input("Booking ID: "))
                print(f"{booking.booking_id} cancelled; seats restored.")
            except ValueError as exc:
                print(f"Cancellation failed: {exc}")
        elif choice == "6":
            only_available = input("Only routes with seats available? (y/n): ").strip().lower() == "y"
            for route in service.get_availability(only_available):
                _print_route(route)
        elif choice == "7":
            for key, value in service.get_report().items():
                print(f"{key.replace('_', ' ').title()}: {value:,}" if isinstance(value, int) else f"{key}: {value}")
        elif choice == "8":
            for city, routes in service.get_schedule().items():
                print(f"\n{city}")
                if not routes:
                    print("  No scheduled departures.")
                for route in routes:
                    print(f"  {route.route_id} -> {route.destination_city} | {route.departure_time}")
        elif choice == "9":
            print("Thank you for using Smart Bus Reservation System.")
            break
        else:
            print("Invalid choice. Choose 1–9.")
