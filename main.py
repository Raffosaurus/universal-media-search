from src.plex import search_plex
from src.tmdb import search_tmdb

def main():
    # Intro label
    print("_____________________________________")
    print("--Welcome to Universal Media Search--")
    print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
    # Get user search terms
    user_search = input("Search by movie or show title: ").lower()
    print(f'\nSearching for "{user_search}"\n')

    # Search Plex - get results from our plex.py module
    plex_results = search_plex(user_search)
    if plex_results:
        print("Plex Results\n‾‾‾‾‾‾‾‾‾‾‾‾")
        for result in plex_results:
            # Check if there are seasons (for shows):
            seasons_info = f" - seasons: {result.seasons}" if result.seasons else ""
            print(f"• {result.title} ({result.year}) - {result.media_type}{seasons_info} [{result.source}]")
        print("_____________________________________\n")
    else:
        print("• No results found on Plex...")

    tmdb_results = search_tmdb(user_search)
    if tmdb_results:
        print("TMDB Results\n‾‾‾‾‾‾‾‾‾‾‾‾")
        for result in tmdb_results:
            print(f"• {result.title} ({result.year}) - {result.media_type} [{result.source}]")
        print("_____________________________________\n")
    else:
        print("• No results found on TMDB...")

if __name__ == "__main__":
    main()
