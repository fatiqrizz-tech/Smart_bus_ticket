# Smart Bus Reservation System — Streamlit UI

A modular Python project with a browser-based Streamlit interface and an optional console interface.

## Run in VS Code (Windows)

1. Extract the ZIP and open the `Smart_Bus_Modular_Project` folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
5. Start the Streamlit UI:
   ```powershell
   python -m streamlit run streamlit_app.py
   ```
6. Open the local URL printed in the terminal (usually `http://localhost:8501`).

Optional console version:
```powershell
python main.py
```

## UI features
- Dashboard with route, booking, seat and revenue metrics
- Route explorer with departure/destination filters and keyword search
- Ticket booking with fare preview and booking confirmation
- Booking history and guarded cancellation
- Seat availability table and chart
- Departure schedule grouped by city
- Reports and CSV export

## Project structure
```text
Smart_Bus_Modular_Project/
├── main.py
├── streamlit_app.py
├── requirements.txt
├── README.md
├── test_cases.txt
└── smart_bus/
    ├── __init__.py
    ├── data.py
    ├── models.py
    ├── services/
    │   ├── __init__.py
    │   ├── reservation_service.py
    │   └── console_app.py
    └── ui/
        ├── __init__.py
        └── streamlit_pages.py
```

## Storage note
As specified by the project requirements, data is stored in memory. Bookings reset when the app/server restarts. This demo does not include a database or payment gateway.
