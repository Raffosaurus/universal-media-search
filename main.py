from src.plex import search_plex
from src.tmdb import search_tmdb
from rich.console import Console
from rich.panel import Panel

 # Iinitialize console:
console = Console()

def print_hero_banner() -> int:
    ascii_art = r"""
╦  ╦                            ╗      ╔═╦═╗       ╦            ╔══╗                 ╦  
║  ║     o                      ║      ║ ║ ║       ║ o          ║                    ║  
║  ║ ╔╗╔ ╦ ╦  ╦ ╔═╗ ╦═╗ ╔═╗ ╔═╗ ║      ║ ║ ║ ╔═╗ ╔═╣ ╦ ╔═╗      ╚══╗ ╔═╗ ╔═╗ ╦═╗ ╔═╗ ╠═╗
║  ║ ║║║ ║ ╚╗╔╝ ╠═╝ ║   ╚═╗ ╔═╣ ║      ║ ║ ║ ╠═╝ ║ ║ ║ ╔═╣         ║ ╠═╝ ╔═╣ ║   ║   ║ ║
╚══╝ ╝╚╝ ╩  ╚╝  ╚═╝ ╩   ╚═╝ ╚═╚ ╩      ╩ ╩ ╩ ╚═╝ ╚═╝ ╩ ╚═╚      ╚══╝ ╚═╝ ╚═╚ ╩   ╚═╝ ╩ ╩
    """

    gradient = [
        "#FD4B29",
        "#FD1D1D",
        "#D9264A",
        "#AD307F",
        "#833AB4",
    ]

    lines = ascii_art.strip("\n").splitlines()

    max_len = max(len(line) for line in lines)

    top_bar = " WELCOME TO ".center(max_len, '━')
    console.print(f"[#FC8038]{top_bar}[/#FC8038]")

    for i, line in enumerate(lines):
        color = gradient[i % len(gradient)]
        console.print(f"[{color}]{line}[/{color}]")

    console.print(f"[#4E249C]{'▔' * max_len}[/#4E249C]")

    return max_len


def main():
    # Intro label
    max_len = print_hero_banner()
    result_endline = "━" * (max_len // 2)
    # Get user search terms
    user_search = console.input("\n[#4E249C]░▒▓[/#4E249C][#833AB4]░[/#833AB4] [bold #627188]Search by movie or show title[/bold #627188] [#FC8038]❯[/#FC8038] ").lower()
    console.print(f'\n[italic #4e5a6c]Searching for "{user_search}"...[/italic #4e5a6c]\n', highlight=False)

    # Search Plex - get results from our plex.py module
    plex_results = search_plex(user_search)

    plex_header = "░▒▓░ Plex Results ".ljust(max_len // 2, '━')
    console.print(f"[#E5A00D]{plex_header}[/#E5A00D]\n")

    if plex_results:
        for result in plex_results:
            print(result)
    else:
        console.print("[italic #4e5a6c]• No results found on Plex......[/italic #4e5a6c]")
    console.print(f"[#E5A00D]{result_endline}[/#E5A00D]")

    tmdb_results = search_tmdb(user_search)

    tmdb_header = "░▒▓░ TMDB Results ".ljust(max_len // 2, '━')
    console.print(f"[#01B4E4]{tmdb_header}[/#01B4E4]\n")
    if tmdb_results:
        for result in tmdb_results:
            print(result)
    else:
        console.print("[italic #01B4E4]• No results found on TMDB......[/italic #01B4E4]")
    console.print(f"[#01B4E4]{result_endline}[/#01B4E4]")

if __name__ == "__main__":
    main()
