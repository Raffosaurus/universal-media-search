import os
import requests
from dotenv import load_dotenv
from src.models import SearchResult


def search_plex(query: str):
    # Open and load .env variables into temp memory
    load_dotenv()

    # Grab .env variables out of temp memory and assign locally
    PLEX_URL = os.getenv("PLEX_URL")
    PLEX_TOKEN = os.getenv("PLEX_TOKEN")

    # Set up instructions for using 'requests' when accessing the Plex server - needs to be dictionary
    plex_headers = {
        "Accept": "application/json",
        "X-Plex-Token": PLEX_TOKEN
    }

    # Search filter setup - needs to be a dictionary
    search_parameters = {
        "query": query,  # our input when calling this function
        "limit": 5          # limit results in case there are too many, ****ADJUST LATER****
    }

    # Setup plex search url and console notification
    plex_url = f"{PLEX_URL}/hubs/search"
    # REMOVE -----> print(f'Attempting Plex search for "{search_parameters["query"]}"...')

    parsed_results = [] # Results from Plex (after formatting)
    # Account for crashes while connecting
    try:
        # Attempt to connect and retrieve data from Plex server
        plex_response = requests.get(plex_url, headers=plex_headers, params=search_parameters, timeout=6)
        # If we connected successfully...
        if plex_response.status_code == 200:
            data = plex_response.json()
            # REMOVE -----> print("Great success! Here are the results:")
            # Clean up `data` into something legible
            hubs = data["MediaContainer"]["Hub"] # media information is stored here, make a list of all `Hub`'s
            for hub in hubs:
                if "Metadata" in hub: # Check hub isn't empty so we don't cause a crash
                    for media in hub["Metadata"]:
                        media_title = media.get("title", "Unknown") # use .get() in case of missing metadata - no crashes
                        media_year = media.get("year", "Unknown")
                        media_type = media.get("type", "Unknown")
                        # Use our `SearchResult` class to hold organized data
                        media_result = SearchResult(title=media_title, year=media_year, media_type=media_type, source="Plex")
                        # Add to our `parsed_results` list
                        parsed_results.append(media_result)
            # REMOVE -----> for result in parsed_results:
                # REMOVE -----> print(f"• {result.title} ({result.year}) - {result.media_type} [{result.source}]")

        # ...and if we connected but there was an error
        else:
            print(f"Whoopsie! Server error... \nStatus code: {plex_response.status_code}")
        
    # Error handling for when we fail to connect
    except requests.exceptions.ConnectTimeout:
        print("Error: Connection timed out! Check if server is on and using the right IP")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return parsed_results