
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return """
    <h2>Weather API</h2>
    <p>Test a city or district:</p>
    <form action="/weather" method="get">
        <input type="text" name="place"
               placeholder="Enter city or district" required>
        <button type="submit">Get Weather</button>
    </form>
    """


# Weather API for cities and districts
@app.route('/weather', methods=['GET'])
def get_weather():

    place_name = request.args.get(
        'place', request.args.get('city', '')
    ).strip()

    if not place_name:
        return jsonify({
            "error": "Please enter a city or district name"
        }), 400

    try:
        # Step 1: Search for the city or district
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_response = requests.get(
            geo_url,
            params={
                "name": place_name,
                "count": 10,
                "language": "en",
                "format": "json"
            },
            timeout=10
        )

        geo_response.raise_for_status()
        geo_data = geo_response.json()

        results = geo_data.get("results", [])

        if not results:
            return jsonify({
                "error": "City or district not found",
                "searched_place": place_name
            }), 404

        # Step 2: Select the first matching place
        place = results[0]
        latitude = place["latitude"]
        longitude = place["longitude"]

        # Step 3: Get current weather
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

        # Step 4: Return the result
        return jsonify({
            "searched_place": place_name,
            "matched_place": place["name"],
            "district_or_area": place.get("admin2", ""),
            "state": place.get("admin1", ""),
            "country": place.get("country", ""),
            "latitude": latitude,
            "longitude": longitude,
            "temperature_celsius": current["temperature_2m"],
            "feels_like_celsius": current["apparent_temperature"],
            "humidity_percent": current["relative_humidity_2m"],
            "wind_speed_kmh": current["wind_speed_10m"],
            "weather_code": current["weather_code"]
        })

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Weather service timed out"
        }), 504

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Unable to connect to weather service",
            "details": str(e)
        }), 502

    except (KeyError, ValueError):
        return jsonify({
            "error": "Invalid response from weather service"
        }), 502


if __name__ == '__main__':
    app.run(debug=True)
