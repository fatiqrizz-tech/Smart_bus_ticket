"""Streamlit UI for the Smart Bus Reservation System."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from smart_bus.data import SUPPORTED_CITIES
from smart_bus.services.reservation_service import ReservationService


def _money(amount: int) -> str:
    return f"Rs. {amount:,}"


def _route_rows(routes) -> pd.DataFrame:
    rows = []
    for route in routes:
        if route.available_seats == 0:
            status = "Fully booked"
        elif route.available_seats == route.total_seats:
            status = "Available"
        else:
            status = "Limited seats"
        rows.append({
            "Route ID": route.route_id,
            "From": route.departure_city,
            "To": route.destination_city,
            "Departure": route.departure_time,
            "Fare": _money(route.ticket_price),
            "Seats left": route.available_seats,
            "Capacity": route.total_seats,
            "Status": status,
        })
    return pd.DataFrame(rows)


def _booking_rows(bookings) -> pd.DataFrame:
    return pd.DataFrame([{
        "Booking ID": b.booking_id,
        "Passenger": b.passenger_name,
        "Age": b.passenger_age,
        "Route": b.route_id,
        "Seats": b.seats,
        "Total fare": _money(b.total_fare),
        "Status": b.status,
    } for b in bookings])


def _style() -> None:
    st.markdown("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
      html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
      .stApp { background: #f5f7fb; }
      [data-testid="stHeader"] { background: rgba(245,247,251,.88); }
      .block-container { padding-top: 1.8rem; padding-bottom: 3rem; max-width: 1450px; }
      [data-testid="stSidebar"] { background: #101b32; }
      [data-testid="stSidebar"] * { color: #eef3ff !important; }
      [data-testid="stSidebar"] [data-testid="stRadio"] label { padding: .45rem .35rem; }
      [data-testid="stMetric"] { background: white; border: 1px solid #e7ebf3; padding: 18px 20px; border-radius: 16px; box-shadow: 0 3px 12px rgba(21,36,68,.035); }
      [data-testid="stMetricLabel"] { color: #667085; font-weight: 600; }
      [data-testid="stMetricValue"] { color: #14213d; font-family: 'Manrope', sans-serif; }
      div.stButton > button, div.stFormSubmitButton > button { border-radius: 10px; font-weight: 700; min-height: 2.65rem; }
      div.stButton > button[kind="primary"], div.stFormSubmitButton > button[kind="primary"] { background: #2357d9; border-color: #2357d9; }
      .hero { background: linear-gradient(115deg,#142344 0%,#2357d9 100%); border-radius: 22px; padding: 28px 30px; color: white; margin-bottom: 22px; box-shadow: 0 12px 28px rgba(35,87,217,.16); }
      .hero h1 { color: white; font-family: 'Manrope',sans-serif; font-size: 2rem; margin: 0 0 7px 0; font-weight: 800; }
      .hero p { color: #dbe7ff; font-size: 1rem; margin: 0; }
      .eyebrow { text-transform: uppercase; letter-spacing: .12em; font-size: .72rem; font-weight: 800; color: #9ebaff; margin-bottom: 8px; }
      .section-note { color: #667085; margin-top: -8px; margin-bottom: 18px; }
      .route-card { background: white; border: 1px solid #e7ebf3; border-radius: 16px; padding: 18px; height: 100%; }
      .route-label { color: #667085; font-size: .78rem; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; }
      .route-cities { color: #14213d; font-family: 'Manrope',sans-serif; font-size: 1.08rem; font-weight: 800; margin: 8px 0; }
      .route-foot { color: #667085; font-size: .88rem; }
      .price { color: #2357d9; font-size: 1.15rem; font-weight: 800; }
      div[data-testid="stDataFrame"] { border: 1px solid #e7ebf3; border-radius: 12px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)


def _hero(kicker: str, title: str, subtitle: str) -> None:
    st.markdown(
        f'<div class="hero"><div class="eyebrow">{kicker}</div>'
        f'<h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def _route_cards(routes) -> None:
    if not routes:
        st.info("No routes match your filters. Try another city or search term.")
        return
    columns = st.columns(min(3, len(routes)))
    for index, route in enumerate(routes):
        with columns[index % len(columns)]:
            status = "Fully booked" if route.available_seats == 0 else f"{route.available_seats} seats available"
            st.markdown(
                f'<div class="route-card"><div class="route-label">{route.route_id} · {route.departure_time}</div>'
                f'<div class="route-cities">{route.departure_city} <span style="color:#2357d9">→</span> {route.destination_city}</div>'
                f'<div class="route-foot">{status} · {route.total_seats} seat capacity</div><hr style="border:0;border-top:1px solid #edf0f6;margin:14px 0">'
                f'<div class="price">{_money(route.ticket_price)} <span style="font-size:.78rem;color:#667085;font-weight:500">/ seat</span></div></div>',
                unsafe_allow_html=True,
            )


def render_app() -> None:
    if "reservation_service" not in st.session_state:
        st.session_state.reservation_service = ReservationService()
    service: ReservationService = st.session_state.reservation_service
    _style()

    with st.sidebar:
        st.markdown("<div style='font-size:2rem;margin:4px 0 0'>🚌</div><h2 style='margin:0;font-family:Manrope,sans-serif'>SmartBus</h2><p style='color:#aab7d1!important;font-size:.85rem;margin-top:4px'>Reservation portal</p>", unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("WORKSPACE", [
            "Dashboard", "Find Routes", "Book Ticket", "Bookings & Cancellation",
            "Seat Availability", "Route Schedule", "Reports",
        ], label_visibility="visible")
        st.markdown("---")
        st.caption("Demo mode · In-memory storage")

    report = service.get_report()
    if page == "Dashboard":
        _hero("SMART TRAVEL, SIMPLIFIED", "Your journey starts here.", "Explore routes, reserve seats, and keep every booking in one place.")
        cols = st.columns(4)
        cols[0].metric("Available routes", len(service.routes))
        cols[1].metric("Total bookings", report["total_bookings"])
        cols[2].metric("Seats reserved", report["reserved_seats"])
        cols[3].metric("Confirmed revenue", _money(report["confirmed_revenue"]))
        st.markdown("### Popular departures")
        st.markdown('<p class="section-note">Browse the routes currently available in the system.</p>', unsafe_allow_html=True)
        _route_cards(service.routes[:3])
        st.markdown("### All routes")
        st.dataframe(_route_rows(service.routes), use_container_width=True, hide_index=True)
        st.info("This project follows the PRD's in-memory storage requirement. Bookings reset when the app/server restarts.")

    elif page == "Find Routes":
        _hero("ROUTE EXPLORER", "Find your next ride", "Search by city or route ID and compare fares before booking.")
        a, b, c = st.columns([1, 1, 1.2])
        with a:
            departure = st.selectbox("Departure city", ["Any city"] + list(SUPPORTED_CITIES))
        with b:
            destination = st.selectbox("Destination city", ["Any city"] + list(SUPPORTED_CITIES))
        with c:
            term = st.text_input("Route ID or keyword", placeholder="e.g. R101 or Lahore")
        matches = service.routes
        if departure != "Any city":
            matches = [r for r in matches if r.departure_city == departure]
        if destination != "Any city":
            matches = [r for r in matches if r.destination_city == destination]
        if term.strip():
            ids = {r.route_id for r in service.search_routes(term)}
            matches = [r for r in matches if r.route_id in ids]
        st.markdown(f"### {len(matches)} route(s) found")
        _route_cards(matches)
        if matches:
            with st.expander("View route details in a table"):
                st.dataframe(_route_rows(matches), use_container_width=True, hide_index=True)

    elif page == "Book Ticket":
        _hero("RESERVATIONS", "Book a ticket", "Enter passenger details, choose a route, and confirm your seats.")
        with st.form("booking_form", clear_on_submit=True):
            left, right = st.columns(2)
            with left:
                passenger_name = st.text_input("Passenger full name", placeholder="Enter passenger name")
                passenger_age = st.number_input("Passenger age", min_value=1, max_value=120, value=18, step=1)
            with right:
                route_ids = [r.route_id for r in service.routes]
                route_id = st.selectbox("Select route", route_ids, format_func=lambda rid: (
                    f"{rid} · {service.get_route(rid).departure_city} → {service.get_route(rid).destination_city}"
                ))
                selected_route = service.get_route(route_id)
                seats = st.number_input("Number of seats", min_value=1, max_value=max(1, selected_route.available_seats), value=1, step=1, disabled=selected_route.available_seats == 0)
            if selected_route.available_seats > 0:
                st.info(f"Departure: **{selected_route.departure_time}**  ·  Fare per seat: **{_money(selected_route.ticket_price)}**  ·  Available: **{selected_route.available_seats}**")
                st.markdown(f"**Estimated total:** {_money(selected_route.ticket_price * int(seats))}")
            else:
                st.warning("This route is fully booked. Please select another route.")
            submitted = st.form_submit_button("Confirm reservation", type="primary", use_container_width=True)
        if submitted:
            try:
                booking = service.book_ticket(passenger_name, int(passenger_age), route_id, int(seats))
                st.success("Your reservation has been confirmed!")
                x, y, z = st.columns(3)
                x.metric("Booking ID", booking.booking_id)
                y.metric("Seats booked", booking.seats)
                z.metric("Total fare", _money(booking.total_fare))
                st.balloons()
            except ValueError as exc:
                st.error(str(exc))

    elif page == "Bookings & Cancellation":
        _hero("MANAGE BOOKINGS", "Your reservations", "Review booking status or cancel a confirmed reservation.")
        bookings = service.list_bookings()
        if bookings:
            st.dataframe(_booking_rows(bookings), use_container_width=True, hide_index=True)
            active = [b.booking_id for b in bookings if b.status == "Confirmed"]
            if active:
                st.markdown("### Cancel a booking")
                selected_id = st.selectbox("Confirmed booking", active, format_func=lambda bid: next(
                    f"{b.booking_id} · {b.passenger_name} · {b.route_id} · {_money(b.total_fare)}" for b in bookings if b.booking_id == bid
                ))
                confirm = st.checkbox("I understand this will cancel the selected booking and release its seats.")
                if st.button("Cancel selected booking", type="primary", disabled=not confirm):
                    try:
                        service.cancel_booking(selected_id)
                        st.success(f"Booking {selected_id} cancelled. Seats have been restored.")
                        st.rerun()
                    except ValueError as exc:
                        st.error(str(exc))
            else:
                st.info("All bookings have been cancelled. There are no active reservations.")
        else:
            st.info("No bookings yet. Visit **Book Ticket** to create your first reservation.")

    elif page == "Seat Availability":
        _hero("LIVE INVENTORY", "Seat availability", "Check remaining capacity before you reserve a seat.")
        only_available = st.toggle("Hide fully booked routes", value=False)
        routes = service.get_availability(only_available)
        st.dataframe(_route_rows(routes), use_container_width=True, hide_index=True)
        if routes:
            chart_data = pd.DataFrame({"Route": [r.route_id for r in routes], "Available seats": [r.available_seats for r in routes]}).set_index("Route")
            st.markdown("### Seats remaining by route")
            st.bar_chart(chart_data)

    elif page == "Route Schedule":
        _hero("DEPARTURE BOARD", "Route schedule", "See departures grouped by their starting city.")
        for city, routes in service.get_schedule().items():
            if routes:
                with st.expander(f"📍 {city} · {len(routes)} departure(s)", expanded=True):
                    st.dataframe(pd.DataFrame([{
                        "Route ID": r.route_id,
                        "Destination": r.destination_city,
                        "Departure time": r.departure_time,
                        "Fare": _money(r.ticket_price),
                        "Seats left": r.available_seats,
                    } for r in routes]), use_container_width=True, hide_index=True)

    elif page == "Reports":
        _hero("BUSINESS OVERVIEW", "Booking reports", "A clear snapshot of reservations, seat usage, and confirmed revenue.")
        cols = st.columns(3)
        cols[0].metric("Total bookings", report["total_bookings"])
        cols[1].metric("Confirmed", report["confirmed_bookings"])
        cols[2].metric("Cancelled", report["cancelled_bookings"])
        cols = st.columns(3)
        cols[0].metric("Seats reserved", report["reserved_seats"])
        cols[1].metric("Confirmed revenue", _money(report["confirmed_revenue"]))
        cols[2].metric("Fully booked routes", report["fully_booked_routes"])
        bookings = service.list_bookings()
        if bookings:
            st.markdown("### Booking history export")
            csv_data = pd.DataFrame([b.to_dict() for b in bookings]).to_csv(index=False).encode("utf-8")
            st.download_button("Download booking history (CSV)", csv_data, file_name="smart_bus_bookings.csv", mime="text/csv", type="primary")
        else:
            st.info("Reports will populate when bookings are created.")

    st.markdown("<div style='text-align:center;color:#8a94a6;font-size:.8rem;padding:28px 0 0'>SmartBus Reservation Portal · Demo project</div>", unsafe_allow_html=True)
