from dataclasses import dataclass, field

@dataclass
class SearchResult:
    title: str
    year: int
    media_type: str  # ex: "movie" or "show"
    source: str      # ex: "Plex", "TMDB"
    seasons: str = "" # default to empty string
    # Can't default an empty dict or list because it's mutable, import and use `field` from dataclasses
    streaming_on: dict = field(default_factory=dict)

    # Dunder method for print (str)
    def __str__(self):
        result_str = f"• {self.title} ({self.year}) - {self.media_type}"
        # Account for seasons in tv shows
        if self.seasons:
            result_str += f" - seasons: {self.seasons}"
        # Loops through dict and prints streaming platforms + regions
        if self.streaming_on:
            for service, countries in self.streaming_on.items():
                country_str = ", ".join(countries)
                result_str += f"\n    ↳ {service} [{country_str}]"

        return result_str