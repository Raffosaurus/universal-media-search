from src.plex import search_plex

def main():
    # Intro label
    print("_____________________________________")
    print("--Welcome to Universal Media Search--")
    print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
    # Get user search terms
    user_search = input("Search by movie or show title: ")
    print(f'\nSearching for "{user_search}"\n')

    # Search Plex - get results from our plex.py module
    plex_results = search_plex(user_search)
    if plex_results:
        print("Plex Results\n‾‾‾‾‾‾‾‾‾‾‾‾")
        for result in plex_results:
            print(f"• {result.title} ({result.year}) - {result.media_type} [{result.source}]")
        print("_____________________________________")
    else:
        print("• No results found on Plex...")
    

if __name__ == "__main__":
    main()


