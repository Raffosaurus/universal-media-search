from dataclasses import dataclass

@dataclass
class SearchResult:
    title: str
    year: int
    media_type: str  # ex: "movie" or "show"
    source: str      # ex: "Plex", "TMDB"
    seasons: str = "" # default to empty string

    # Dunder method for print (str)
    def __str__(self):
        result_str = f"• {self.title} ({self.year}) - {self.media_type}"
        # Account for seasons in tv shows
        if self.seasons:
            result_str += f" - seasons: {self.seasons}"

        return result_str