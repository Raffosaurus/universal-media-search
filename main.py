import os
import requests
from dotenv import load_dotenv

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

# Search filter setup - needs to be dictionary
search_parameters = {
    "query": "Batman",  # hardcoded search for testing
    "limit": 5          # limit results in case there are too many, ****ADJUST LATER****
}

# Setup plex search url and console notification
plex_url = f"{PLEX_URL}/hubs/search"
print(f'Attempting Plex search for "{search_parameters["query"]}"...')

# Account for crashes while connecting
try:
    # Attempt to connect and retrieve data from Plex server
    plex_response = requests.get(plex_url, headers=plex_headers, params=search_parameters, timeout=6)
    # If we connected successfully...
    if plex_response.status_code == 200:
        data = plex_response.json()
        print("Great success! Here is the raw result:")
        print(data)
    # ...and if we connected but there was an error
    else:
        print(f"Whoopsie! Server error... \nStatus code: {plex_response.status_code}")
    
# Error handling for when we fail to connect
except requests.exceptions.ConnectTimeout:
    print("Error: Connection timed out! Check if server is on and using the right IP")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")






# ****REMOVE AFTER SEARCH TEST****
# Previous "server knock" test

# # Set up plex url and console notification
# plex_url = f"{PLEX_URL}/identity"
# print(f"Attempting to connect to: {plex_url}")

# # Account for crashes while connecting
# try:
#     # Attempt to connect and retrieve data from Plex server
#     plex_response = requests.get(plex_url, headers=plex_headers, timeout=6)
#     # If we connected sucessfully...
#     if plex_response.status_code == 200:
#         print("Great success! Here is the server data:")
#         print(plex_response.json())
#     # ...and if we connected but there was an error
#     else:
#         print(f"Whoops! Server error... Status Code: {plex_response.status_code}")

# # Error handling for when we fail to connect
# except requests.exceptions.ConnectTimeout:
#     print("Error: Connection timed out! Check if server is on and using the right IP")
# except requests.exceptions.RequestException as e:
#     print(f"A general network error occurred: {e}")