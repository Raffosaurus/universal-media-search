import os
import requests
from dotenv import load_dotenv
from src.models import SearchResult

#================
# Global setup
load_dotenv() # Open and load .env variables into temp memory
PLEX_URL = os.getenv("PLEX_URL") # Grab .env variables out of temp memory and assign locally
PLEX_TOKEN = os.getenv("PLEX_TOKEN")

# Set up instructions for using 'requests' when accessing the Plex server - needs to be dictionary
PLEX_HEADERS = {
    "Accept": "application/json",
    "X-Plex-Token": PLEX_TOKEN
}
#================

# Helper function -> parse_plex_data() - look up and return available seasons
def get_show_seasons(rating_key: str) -> list:
    # Set up plex season search URL
    season_url = f"{PLEX_URL}/library/metadata/{rating_key}/children"
    media_seasons = [] # season results from Plex after formatting

    # Test for crashes while trying to connect
    try:
        # Try to connect and retreive data from Plex server
        season_response = requests.get(season_url, headers=PLEX_HEADERS, timeout=5)
        # If we connect successfully...
        if season_response.status_code == 200:
            season_data = season_response.json()
            # Look in the correct area for season details
            season_hubs = season_data.get("MediaContainer", {}).get("Metadata", [])
            for s_hub in season_hubs:
                season_num = s_hub.get("index") # Parse the season number
                if season_num and season_num > 0: # Plex uses 'season 0' as bonus features/extras - ignore these 
                    media_seasons.append(str(season_num))

        else:
            print(f"Whoopsie! Server error getting seasons... \nStatus code: {season_response.status_code}")
                
    except requests.exceptions.ConnectTimeout:
        print("Error: Connection timed out! Check if server is on and using the right IP")
    except requests.exceptions.RequestException as e:
        print(f'Server error while trying to get season data: {e}')

    return media_seasons

# Helper funciton -> search_plex() - clean up `data` into sometihng legible
def parse_plex_data(data: dict, query: str) -> list:
    parsed_results = [] # Results from Plex (after formatting)
    # Access Hub list in the Plex JSON dictionary safely - no crashes
    hubs = data.get("MediaContainer", {}).get("Hub", [])

    for hub in hubs:
        hub_type = hub.get("type") # Look up the media type
        if hub_type not in ["movie", "show"]: # Media type filter
            continue
        if "Metadata" in hub: # Check hub isn't empty so we don't cause a crash
            for media in hub["Metadata"]:
                media_title = media.get("title", "Unknown") # use .get() in case of missing metadata - no crashes
                media_sort_title = media.get("titleSort", "") # needed for filtering
                if query not in media_title.lower() and query not in media_sort_title.lower(): # Only return results with query in the Title or Sort Title
                    continue
                media_year = media.get("year", "Unknown")
                media_type = media.get("type", "Unknown")
                media_type = "tv" if media_type == "show" else media_type # Unify output to match TMDB - looks cleaner in console output
                media_seasons = []
                if hub_type == "show" and media.get("ratingKey"):
                    media_seasons = get_show_seasons(media.get("ratingKey"))
                
                formatted_media_seasons = ", ".join(media_seasons)
                # Use our `SearchResult` class to hold organized data
                media_result = SearchResult(
                    title=media_title,
                    year=media_year,
                    media_type=media_type,
                    source="Plex",
                    seasons=formatted_media_seasons
                )
                # Add to our `parsed_results` list
                parsed_results.append(media_result)
    return parsed_results
    

# Main plex search function
def search_plex(query: str):
    # Search filter setup - needs to be a dictionary
    search_parameters = {
        "query": query,  # our input when calling this function
        "limit": 6          # limit results in case there are too many
    }

    # Setup plex search url and console notification
    plex_url = f"{PLEX_URL}/hubs/search"

    parsed_results = [] # Results from Plex (after formatting)
    # Account for crashes while connecting
    try:
        # Attempt to connect and retrieve data from Plex server
        plex_response = requests.get(plex_url, headers=PLEX_HEADERS, params=search_parameters, timeout=5)
        # If we connected successfully...
        if plex_response.status_code == 200:
            data = plex_response.json()

            parsed_results = parse_plex_data(data, query)

        # ...and if we connected but there was an error
        else:
            print(f"Whoopsie! Server error... \nStatus code: {plex_response.status_code}")
        
    # Error handling for when we fail to connect
    except requests.exceptions.ConnectTimeout:
        print("Error: Connection timed out! Check if server is on and using the right IP")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return parsed_results