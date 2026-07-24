from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "prompt_label": "bold #7A899E",
    "status_text": "dim italic #627188",
    "subtext": "italic #505F75",
    "plex_brand": "bold #E5A00D",
    "tmdb_brand": "bold #01B4E4",
    "accent": "#FC8038",
    "seasons": "dim italic #FC8038",
    "bg_dark": "#4E249C",
    "title": "bold white",
    "netflix": "bold #E50914",
    "prime": "bold #00A8E1",
    #"hulu": "bold #1CE783",
    #"disney": "bold #113CCF",
    #"max": "bold #9A2EE0", 
    #"apple": "bold #D6D6D6",
})

# Iinitialize console:
console = Console(theme=custom_theme)

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
    console.print(f"\n[#FC8038]{top_bar}[/#FC8038]")

    for i, line in enumerate(lines):
        color = gradient[i % len(gradient)]
        console.print(f"[{color}]{line}[/{color}]")

    console.print(f"[#4E249C]{'▔' * max_len}[/#4E249C]")

    return max_len