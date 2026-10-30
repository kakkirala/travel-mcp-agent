# Travel Planner — MCP Travel Agent

An AI travel-planning assistant that plans trips in plain words. A Model
Context Protocol (MCP) server holds the travel tools, a LangChain + Groq
agent discovers and calls those tools, and a FastAPI web page gives you a
MakeMyTrip-style search experience.

## What it does

- **Day-by-day itineraries** for Kyoto, Tokyo, Kuala Lumpur, and Kochi
- **Flight search** — cheapest first, with sort by cheapest, fastest, and
  fewest stops, plus a demo Book Now flow
- **Hotel search** — cheapest first, with price per night, rating, stay
  total, and a demo Book Now flow
- **Budget estimates** — daily rate × days × travellers, with a trip total
- **Search page** — From / To dropdowns, One Way / Round Trip / Multi City,
  travel dates, days, and travellers
- **Follow-up chat** — refine the same plan ("make it 5 days", "add more
  shopping") without starting over
- **Download plan** — save the finished plan as a text file
- **Booking review pages** — traveller / guest details with a per-person
  fare breakup (demo only — no real booking or payment)

> All fares, hotels, and budgets are **example data for demo**, not live
> prices or availability.

## Tools (MCP server)

| Tool | What it does |
| --- | --- |
| `search_destination` | Details for a sample city |
| `create_itinerary` | Day-by-day plan for a city |
| `budget_estimate` | Stay budget from daily rate × days × travellers |
| `search_flights` | Sample fares from New York (JFK), cheapest first |
| `search_hotels` | Sample stays, cheapest first |

## Run it

You need a Groq API key (free at console.groq.com).

**Terminal 1 — MCP server (port 8000):**

```powershell
python mcp_server.py
