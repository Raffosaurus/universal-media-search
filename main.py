from src.plex import search_plex
from src.tmdb import search_tmdb
from rich.console import Console
from rich.panel import Panel

from src.ui import console, print_hero_banner


def main():
    # Intro label
    max_len = print_hero_banner()
    result_endline = "━" * (max_len)
    # Get user search terms
    user_search = console.input("\n[bg_dark]░▒▓[/bg_dark][#833AB4]░[/#833AB4] [prompt_label]Search by movie or show title[/prompt_label] [accent]❯[/accent] ").lower()
    console.print(f'\n[status_text]...Searching for "{user_search}"...[/status_text]\n\n', highlight=False)

    # Search Plex - get results from our plex.py module
    plex_results = search_plex(user_search)

    plex_header = "░▒▓░ Plex Results ".ljust(max_len, '━')
    console.print(f"[plex_brand]{plex_header}[/plex_brand]\n")

    if plex_results:
        for result in plex_results:
            console.print(result, highlight=False)
    else:
        console.print("[subtext]• No results found on Plex...[/subtext]")
    console.print(f"[plex_brand]{result_endline}[/plex_brand]\n")

    tmdb_results = search_tmdb(user_search)

    tmdb_header = "░▒▓░ TMDB Results ".ljust(max_len, '━')
    console.print(f"[tmdb_brand]{tmdb_header}[/tmdb_brand]\n")
    if tmdb_results:
        for result in tmdb_results:
            console.print(result, highlight=False)
    else:
        console.print("[subtext]• No results found on TMDB...[/subtext]")
    console.print(f"[tmdb_brand]{result_endline}[/tmdb_brand]\n")

if __name__ == "__main__":
    main()
