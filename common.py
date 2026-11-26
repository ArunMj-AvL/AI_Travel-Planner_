"""Shared input and configuration for the four travel-planner lessons.

Students learn input checking once and reuse it in all four frameworks.
No API request happens here. A request happens only when a demo runs its model.
"""

import argparse  # Turn terminal options into named Python values.
import os  # Read settings without putting a secret key in Python code.
from pathlib import Path  # Find .env relative to this file.
from dotenv import load_dotenv  # Read KEY=value lines from local settings.

# These optional services are unnecessary for this classroom project.
# Set flags before the lesson scripts import their AI frameworks.
os.environ.setdefault("CREWAI_TELEMETRY_DISABLED", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")
os.environ.setdefault("LANGSMITH_TRACING", "false")
os.environ.setdefault("LANGCHAIN_TRACING_V2", "false")
# CrewAI creates small internal files even without conversational memory.
os.environ.setdefault("CREWAI_STORAGE_DIR", str(Path(__file__).resolve().with_name(".crewai")))
load_dotenv(Path(__file__).with_name(".env"), override=False)  # Terminal settings win.


def read_trip(allow_offline=False):
    """Read and validate terminal input for one person's local trip.

    Args: allow_offline adds --offline only for the LangGraph lesson.
    Returns: an argparse Namespace with destination, days, budget and optionally offline.
    Invalid input stops here, before an API request can cost money.
    """
    parser = argparse.ArgumentParser(description="Plan a simple practice trip.")
    parser.add_argument("--destination", default="Goa", help="City to explore")
    parser.add_argument("--days", type=int, default=3, help="Trip length: 1 to 7")
    parser.add_argument("--budget", type=int, default=15000, help="Total budget in INR")
    if allow_offline:  # Other demos always use a real language model.
        parser.add_argument("--offline", action="store_true", help="Skip the AI writer")
    trip = parser.parse_args()  # Convert --days 3 into trip.days.
    trip.destination = trip.destination.strip()  # Remove outside spaces.
    if not trip.destination or len(trip.destination) > 80:
        parser.error("Destination must contain 1 to 80 characters.")
    if not 1 <= trip.days <= 7:
        parser.error("Days must be between 1 and 7.")
    if trip.budget <= 0:
        parser.error("Budget must be a positive whole number in INR.")
    return trip  # Every lesson receives checked inputs.


def model_settings():
    """Return the API key and model name, or explain a missing setting.

    The key is returned to framework clients; it is never printed.
    All lessons use a standard OpenAI key and endpoint.
    """
    key = os.getenv("OPENAI_API_KEY", "").strip()  # Read the local secret.
    if not key or key == "your_openai_api_key_here":
        raise ValueError("Add OPENAI_API_KEY to this project's .env before running.")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()  # Small teaching default.
    if not model:
        raise ValueError("OPENAI_MODEL cannot be empty.")
    return key, model  # The caller unpacks this two-item tuple.


def trip_brief(trip):
    """Return the same plain-text task for the three model-driven comparisons.

    Input is the checked Namespace. Output is a string for one traveller.
    Prices are estimates; no lesson searches booking services.
    """
    return (
        f"Plan a {trip.days}-day trip to {trip.destination} for one person. "
        f"Total budget: INR {trip.budget}. Include a short day-by-day itinerary, "
        "estimated local stay, food and activity costs, and a budget warning if needed. "
        "Exclude travel to and from the destination. Use at most 180 words."
    )
