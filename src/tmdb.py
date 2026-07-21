import requests
import os
from dotenv import load_dotenv
from src.models import SearchResult

# ==========================================
# USER CONFIGURATION: STREAMING SERVICES
#
# Add the TMDB provider IDs to `MY_PROVIDER_IDS` for the streaming services you subscribe to.
# 
# Common US IDs:
# 8    = Netflix
# 9    = Amazon Prime Video
# 15   = Hulu
# 337  = Disney+
# 350  = Apple TV
# 1899 = HBO Max
# ==========================================
MY_PROVIDER_IDS = [8, 9]
HOME_REGION = "US"

load_dotenv()
TMDB_API = os.getenv("TMDB_API_KEY")

def get_stream_providers(item_id: int, media_type: str):
    provider_url = f"https://api.themoviedb.org/3/{media_type}/{item_id}/watch/providers"

    search_parameters = {"api_key": TMDB_API,}

    providers = {}
    try:
        tmdb_response = requests.get(url=provider_url, params=search_parameters, timeout=(3.05, 15))
        tmdb_response.raise_for_status()

        providers = tmdb_response.json()
    except requests.exceptions.RequestException as e:
        print(f"TMDB search failed: {e}")
        return None
    
    return providers




def parse_tmdb_data(data: dict):
    parsed_results = [] # Results from TMDB after formatting

    items = data.get("results", []) # TMDB JSON lists search result items in "results" dict

    for item in items[:3]:
        media_type = item.get("media_type") # get the media type of each results in order to use filter
        if media_type not in ["movie", "tv"]: # filter our any result that isn't a movie or TV show
            continue

        # Handle naming discrepency
            # TMDB labels movie titles as "title" but show titles as "name"
            # TMDB labels release date for movies as "release_date", and "first_air_date" for shows
            # Full dates (YYYY-MM-DD) are provided, not just year
        if media_type == "movie":
            media_title = item.get("title", "Unknown Title")
            full_date = item.get("release_date", "")
        else:
            media_title = item.get("name", "Unknown Title")
            full_date = item.get("first_air_date", "")
        media_date = full_date[:4] if full_date else "Unknown"

        item_id = item.get("id")
        provider_data = get_stream_providers(item_id=item_id, media_type=media_type)
        all_countries = provider_data.get("results", {})
        available_on = {}
        for country_code, country_data in all_countries.items():
            streaming_services = country_data.get("flatrate", [])

            for service in streaming_services:
                if service.get("provider_id") in MY_PROVIDER_IDS:
                    provider_name = service.get("provider_name")

                    if provider_name not in available_on:
                        available_on[provider_name] = []
                    
                    available_on[provider_name].append(country_code)
        for service, countries in available_on.items():
            if HOME_REGION in countries:
                available_on[service] = [HOME_REGION]
            else:
                available_on[service] = countries[:4]
        
        if not available_on:
            continue

        # Use our `SearchResult` class to hold organized data
        media_result = SearchResult(
            title=media_title,
            year=media_date,
            media_type=media_type,
            source="TMDB",
            streaming_on=available_on
        )

        parsed_results.append(media_result)
    
    return parsed_results[:6] # Only return the top 6 results



def search_tmdb(query: str):
    tmdb_url = "https://api.themoviedb.org/3/search/multi"

    search_parameters = {
        "api_key": TMDB_API,
        "query": query,
        "include_adult": "false"
    }

    parsed_results = []

    try:
        tmdb_response = requests.get(tmdb_url, params=search_parameters, timeout=(3.05, 15))
        tmdb_response.raise_for_status()

        data = tmdb_response.json()
        parsed_results = parse_tmdb_data(data)
    
    except requests.exceptions.RequestException as e:
        print(f"TMDB search failed: {e}")
        return None
    
    return parsed_results