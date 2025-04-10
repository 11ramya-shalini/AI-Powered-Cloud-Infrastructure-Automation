import requests
import random

AMAD_API_KEY = "ZsKcmg4nI9fXV4d38jLk4kALWAr00Hlr"
AMAD_API_SECRET = "WMM4wfTXJGkW6Y2Q"

def get_amadeus_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': AMAD_API_KEY,
        'client_secret': AMAD_API_SECRET
    }
    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
    
    response = requests.post(url, data=payload, headers=headers)
    return response.json().get('access_token')

def fetch_hotels_in_bangkok():
    access_token = get_amadeus_token()
    if not access_token:
        print("❌ Failed to get access token")
        return []

    headers = { "Authorization": f"Bearer {access_token}" }
    params = {
        "latitude": 13.7563,
        "longitude": 100.5018,
        "radius": 5,
        "radiusUnit": "KM",
        "hotelSource": "ALL"
    }
    url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-geocode"
    
    response = requests.get(url, headers=headers, params=params)

    try:
        json_data = response.json()
        print("✅ Raw API Response:")
        print(json_data)
    except Exception as e:
        print("❌ Failed to parse JSON:", e)
        return []

    hotels = json_data.get("data", [])
    
    hotel_list = []
    for hotel in hotels:
        raw_name = hotel.get("name", "Unnamed Hotel")
        name = raw_name["content"] if isinstance(raw_name, dict) and "content" in raw_name else raw_name

        distance_data = hotel.get("distance", {})
        distance = round(distance_data.get("value", 1.0), 2) if isinstance(distance_data, dict) else 1.0

        hotel_list.append({
            "name": name,
            "rating": round(random.uniform(3.5, 5.0), 1),   # Mock rating
            "price": random.randint(50, 200),     # Mock price
            "city_name": hotel.get("iatacode","Bangkok"),
            "distance": distance
        })

    print("🏨 Final hotel list passed to AI logic:")
    for h in hotel_list:
        print(h)
    return hotel_list
