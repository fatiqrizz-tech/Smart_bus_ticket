"""Seed data for the application. Values follow the supplied PRD."""
from smart_bus.models import Route

def get_initial_routes():
    return [
        Route("R101", "Karachi", "Hyderabad", "08:00 AM", 1200, 40, 40),
        Route("R102", "Karachi", "Sukkur", "09:30 AM", 2000, 36, 36),
        Route("R103", "Hyderabad", "Mirpur Khas", "11:00 AM", 800, 32, 32),
        Route("R104", "Karachi", "Lahore", "07:00 PM", 5000, 45, 45),
        Route("R105", "Sukkur", "Hyderabad", "02:00 PM", 1500, 30, 30),
    ]

SUPPORTED_CITIES = ("Karachi", "Hyderabad", "Sukkur", "Mirpur Khas", "Lahore")
