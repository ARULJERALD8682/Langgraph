
from langchain.tools import tool
import requests

@tool
def search_flight(departure_id: str, arrival_id: str, outbound_date: str):
    """
        A tool that fetches flights for a specific date which is given by the user.
        Args:
            departure_id (str): Origin airport IATA code (e.g., "MAA" for Chennai).
            arrival_id (str): Destination airport IATA code (e.g., "TRZ" for Trichy).
            outbound_date (str): The date the user wants to search flights for.
        
        Returns:
            str: A string representation of available flights or an error message.
        """
    response = requests.get(
        "https://serpapi.com/search?engine=google_flights", 
        params={
            "departure_id": departure_id, 
            "arrival_id": arrival_id, 
            "type": 2,
            "api_key": "73cb4a2322d64c04b01c13b9c4ebca216df9e67bcb39975bd365d62f97403fc1", 
            "outbound_date": outbound_date
        }
    )
    try:
        if response.status_code == 200:
            data = response.json()
            if data.get("best_flights") or data.get("other_flights"):
                flights = [
                    {
                        "Departure_place": best_flights.get("flights")[0].get("departure_airport").get("name"),
                        "Departure_time": best_flights.get("flights")[0].get("departure_airport").get("time"),
                        "Arrival_place": best_flights.get("flights")[0].get("arrival_airport").get("name"),
                        "Arrival_time": best_flights.get("flights")[0].get("arrival_airport").get("time"),
                        "Total_duration": best_flights.get("total_duration"),
                        "Price": best_flights.get("price")
                    }
                    for best_flights in data.get("best_flights")
                ]
                print(flights)
                return str(flights)  # Convert the list of flights to a string representation
            else:
                return "API didn't return any flights. Please check if flights are available."
        else:
            return f"Error: Received a {response.status_code} status code from the API."
    except Exception as e:
        return f"Error fetching flights: {e}"