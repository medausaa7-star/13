
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Weather API is running! Use /weather?city=Bengaluru"


@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', 'Bengaluru').strip()

    # City name to latitude and longitude
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    try:
        geo_response = requests.get(
            geo_url,
            params={
                "name": city,

                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=10
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return jsonify({"error": "City not found"}), 404

        place = geo_data["results"][0]
        latitude = place["latitude"]
        longitude = place["longitude"]

        # Get current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_response = requests.get(
            weather_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "apparent_temperature,"
                    "wind_speed_10m,"
                    "weather_code"
                )
            },
            timeout=10
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data["current"]

        return jsonify({
            "city": place["name"],
            "country": place.get("country", ""),
            "temperature": current["temperature_2m"],
            "feels_like": current["apparent_temperature"],
            "humidity": current["relative_humidity_2m"],
            "wind_speed": current["wind_speed_10m"],
            "weather_code": current["weather_code"]
        })

    except requests.exceptions.RequestException:
        return jsonify({
            "error": "Unable to connect to the weather service"
        }), 502


if __name__ == '__main__':
    app.run(debug=True)
