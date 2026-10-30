from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Counts AI Travel Planner", json_response=True)

DESTINATIONS = {
    "kyoto": {
        "country": "Japan",
        "highlights": ["temples", "gardens", "traditional streets", "local food"],
        "best_for": ["culture", "history", "food", "relaxed trips"],
    },
    "tokyo": {
        "country": "Japan",
        "highlights": ["city views", "food markets", "temples", "shopping"],
        "best_for": ["city breaks", "food", "culture", "families"],
    },
    "kuala lumpur": {
        "country": "Malaysia",
        "highlights": ["food markets", "city views", "museums", "shopping"],
        "best_for": ["food", "city breaks", "families"],
    },
    "kochi": {
        "country": "India",
        "highlights": ["Fort Kochi", "heritage streets", "waterfront", "Kerala cuisine"],
        "best_for": ["culture", "food", "slow travel"],
    },
}

DAILY_RATES = {
    "kyoto": 120,
    "tokyo": 150,
    "kuala lumpur": 80,
    "kochi": 60,
}

FLIGHTS = {
    "tokyo": [
        {"airline": "Example Airlines", "from": "New York (JFK)", "to": "Tokyo (HND)", "price_usd": 780, "stops": 1, "duration": "16h 10m"},
        {"airline": "Demo Air", "from": "New York (JFK)", "to": "Tokyo (HND)", "price_usd": 920, "stops": 0, "duration": "14h 05m"},
        {"airline": "Sample Airways", "from": "New York (JFK)", "to": "Tokyo (HND)", "price_usd": 1050, "stops": 1, "duration": "18h 40m"},
    ],
    "kyoto": [
        {"airline": "Example Airlines", "from": "New York (JFK)", "to": "Osaka (KIX)", "price_usd": 810, "stops": 1, "duration": "16h 50m"},
        {"airline": "Demo Air", "from": "New York (JFK)", "to": "Osaka (KIX)", "price_usd": 940, "stops": 0, "duration": "14h 30m"},
        {"airline": "Sample Airways", "from": "New York (JFK)", "to": "Osaka (KIX)", "price_usd": 1100, "stops": 1, "duration": "19h 15m"},
    ],
    "kuala lumpur": [
        {"airline": "Example Airlines", "from": "New York (JFK)", "to": "Kuala Lumpur (KUL)", "price_usd": 890, "stops": 1, "duration": "20h 25m"},
        {"airline": "Demo Air", "from": "New York (JFK)", "to": "Kuala Lumpur (KUL)", "price_usd": 1010, "stops": 0, "duration": "18h 10m"},
        {"airline": "Sample Airways", "from": "New York (JFK)", "to": "Kuala Lumpur (KUL)", "price_usd": 1180, "stops": 2, "duration": "23h 05m"},
    ],
    "kochi": [
        {"airline": "Example Airlines", "from": "New York (JFK)", "to": "Kochi (COK)", "price_usd": 950, "stops": 1, "duration": "19h 45m"},
        {"airline": "Demo Air", "from": "New York (JFK)", "to": "Kochi (COK)", "price_usd": 1080, "stops": 1, "duration": "21h 20m"},
        {"airline": "Sample Airways", "from": "New York (JFK)", "to": "Kochi (COK)", "price_usd": 1240, "stops": 2, "duration": "24h 30m"},
    ],
}

HOTELS = {
    "tokyo": [
        {"name": "Demo Inn Tokyo Station", "area": "Tokyo Station", "price_per_night_usd": 110, "rating": 4.2},
        {"name": "Example Hotel Shinjuku", "area": "Shinjuku", "price_per_night_usd": 140, "rating": 4.5},
        {"name": "Sample Stay Ginza", "area": "Ginza", "price_per_night_usd": 180, "rating": 4.7},
    ],
    "kyoto": [
        {"name": "Demo Inn Kyoto Station", "area": "Kyoto Station", "price_per_night_usd": 90, "rating": 4.1},
        {"name": "Example Hotel Gion", "area": "Gion", "price_per_night_usd": 120, "rating": 4.4},
        {"name": "Sample Stay Arashiyama", "area": "Arashiyama", "price_per_night_usd": 150, "rating": 4.6},
    ],
    "kuala lumpur": [
        {"name": "Demo Inn Bukit Bintang", "area": "Bukit Bintang", "price_per_night_usd": 60, "rating": 4.0},
        {"name": "Example Hotel KLCC", "area": "KLCC", "price_per_night_usd": 95, "rating": 4.4},
        {"name": "Sample Stay Chinatown", "area": "Chinatown", "price_per_night_usd": 130, "rating": 4.6},
    ],
    "kochi": [
        {"name": "Demo Inn Fort Kochi", "area": "Fort Kochi", "price_per_night_usd": 50, "rating": 4.1},
        {"name": "Example Hotel Marine Drive", "area": "Marine Drive", "price_per_night_usd": 75, "rating": 4.3},
        {"name": "Sample Stay Backwaters", "area": "Backwaters", "price_per_night_usd": 110, "rating": 4.5},
    ],
}

@mcp.tool()
def search_destination(destination: str) -> dict:
    """Find example travel ideas for a destination by city name."""
    key = destination.strip().lower()
    result = DESTINATIONS.get(key)
    if not result:
        return {
            "found": False,
            "destination": destination,
            "available_examples": sorted(DESTINATIONS.keys()),
            "message": "No example entry. Ask for another city.",
        }
    return {"found": True, "destination": destination, **result}

@mcp.tool()
def create_itinerary(destination: str, days: int, interests: list[str]) -> dict:
    """Create a draft itinerary from example data; no live travel data."""
    if days < 1 or days > 14:
        return {"error": "days must be between 1 and 14"}
    info = DESTINATIONS.get(destination.strip().lower())
    if not info:
        return {
            "error": "Destination not in example dataset",
            "available_examples": sorted(DESTINATIONS.keys()),
        }
    plan = []
    for day in range(1, days + 1):
        highlight = info["highlights"][(day - 1) % len(info["highlights"])]
        plan.append({
            "day": day,
            "theme": highlight,
            "interest_match": [item for item in interests if item.lower() in info["best_for"] or item.lower() in highlight.lower()],
            "suggestion": f"Explore {highlight} in {destination}; allow time for breaks.",
        })
    return {
        "destination": destination,
        "days": plan,
        "data_note": "Illustrative plan only; verify current details.",
    }

@mcp.tool()
def budget_estimate(destination: str, days: int, travelers: int = 1) -> dict:
    """Estimate trip cost from example daily rates; no live prices."""
    if days < 1 or days > 14:
        return {"error": "days must be between 1 and 14"}
    if travelers < 1:
        return {"error": "travelers must be at least 1"}
    rate = DAILY_RATES.get(destination.strip().lower())
    if not rate:
        return {
            "error": "Destination not in example dataset",
            "available_examples": sorted(DAILY_RATES.keys()),
        }
    return {
        "destination": destination,
        "days": days,
        "travelers": travelers,
        "daily_rate_usd": rate,
        "estimated_total_usd": rate * days * travelers,
        "assumptions": "Sample daily rate covers stay, food and local travel per person; flights and shopping not included. Illustrative only, not live prices.",
    }

@mcp.tool()
def search_flights(destination: str) -> dict:
    """Find example flights to a city, cheapest first; no live fares."""
    key = destination.strip().lower()
    options = FLIGHTS.get(key)
    if not options:
        return {
            "found": False,
            "destination": destination,
            "available_examples": sorted(FLIGHTS.keys()),
            "message": "No example flights. Ask for another city.",
        }
    cheapest_first = sorted(options, key=lambda f: f["price_usd"])
    return {
        "found": True,
        "destination": destination,
        "flights": cheapest_first,
        "data_note": "Sample fares only, sorted cheapest first; not live prices or availability.",
    }

@mcp.tool()
def search_hotels(destination: str) -> dict:
    """Find example hotels in a city, cheapest first; no live availability."""
    key = destination.strip().lower()
    options = HOTELS.get(key)
    if not options:
        return {
            "found": False,
            "destination": destination,
            "available_examples": sorted(HOTELS.keys()),
            "message": "No example hotels. Ask for another city.",
        }
    cheapest_first = sorted(options, key=lambda h: h["price_per_night_usd"])
    return {
        "found": True,
        "destination": destination,
        "hotels": cheapest_first,
        "data_note": "Sample prices only, sorted cheapest first; not live availability or booking.",
    }

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
