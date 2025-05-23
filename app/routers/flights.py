from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.forms import SearchForm
import requests
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/search", response_class=HTMLResponse)
async def search_form(request: Request):
    form = SearchForm()
    return templates.TemplateResponse("search.html", {"request": request, "form": form})

@router.post("/search", response_class=HTMLResponse)
async def search_flights(
    request: Request,
    departure: str = Form(...),
    destination: str = Form(...),
    date: str = Form(...)
):
    # получение токена
    auth_response = requests.post(
        "https://test.api.amadeus.com/v1/security/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": "tjXn6Rxj68O0InIYHJWjpYXiUzit1WQW",
            "client_secret": "IvLI8ysZA7D6SIxD"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    auth_data = auth_response.json()
    access_token = auth_data["access_token"]

    # запрос к Flight Offers Search
    flight_response = requests.get(
        "https://test.api.amadeus.com/v2/shopping/flight-offers",
        headers={"Authorization": f"Bearer {access_token}"},
        params={
            "originLocationCode": departure.upper(),
            "destinationLocationCode": destination.upper(),
            "departureDate": date,
            "adults": 1,
            "max": 5
        }
    )
    response_data = flight_response.json()
    flights = response_data.get("data", [])
    dictionaries = response_data.get("dictionaries", {})

    # преобразование данных для шаблона
    formatted_flights = []
    for flight in flights:
        for itinerary in flight.get("itineraries", []):
            for segment in itinerary.get("segments", []):
                departure_time = datetime.strptime(segment["departure"]["at"], "%Y-%m-%dT%H:%M:%S")
                arrival_time = datetime.strptime(segment["arrival"]["at"], "%Y-%m-%dT%H:%M:%S")
                formatted_flight = {
                    "flight_number": f"{segment['carrierCode']}{segment['number']}",
                    "departure": segment["departure"]["iataCode"],
                    "destination": segment["arrival"]["iataCode"],
                    "departure_time": departure_time.strftime("%Y-%m-%d %H:%M"),
                    "arrival_time": arrival_time.strftime("%Y-%m-%d %H:%M"),
                    "carrier": dictionaries.get("carriers", {}).get(segment["carrierCode"], segment["carrierCode"]),
                    "price": flight["price"]["total"],
                    "currency": flight["price"]["currency"]
                }
                formatted_flights.append(formatted_flight)

    return templates.TemplateResponse("search.html", {"request": request, "flights": formatted_flights, "form": SearchForm()})