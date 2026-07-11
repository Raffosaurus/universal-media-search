from dataclasses import dataclass

@dataclass
class SearchResult:
    title: str
    year: int
    media_type: str  # ex: "movie" or "show"
    source: str      # ex: "Plex", "TMDB", "Netflix"
    seasons: str = "" # default to empty string