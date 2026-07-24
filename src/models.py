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
    def __rich__(self):
        result_str = f"[status_text]•[/status_text] [title]{self.title}[/title] [subtext]({self.year})[/subtext] [status_text]-[/status_text] [subtext]{self.media_type}[/subtext]"
        # Account for seasons in tv shows
        if self.seasons:
            result_str += f"\n    [status_text]↳[/status_text] [subtext]Seasons: {self.seasons}[/subtext]"
        # Loops through dict and prints streaming platforms + regions
        if self.streaming_on:
            for service, countries in self.streaming_on.items():
                country_str = ", ".join(countries)

                # Brand matcher =====
                brand_tag = "bold white" 
                if "Netflix" in service:
                    brand_tag = "netflix"
                elif "Amazon" in service or "Prime" in service:
                    brand_tag = "prime"
                #elif "Hulu" in service:
                    #brand_tag = "hulu"
                #elif "Disney" in service:
                    #brand_tag = "disney"
                #elif "Max" in service or "HBO" in service:
                    #brand_tag = "max"
                #elif "Apple" in service:
                    #brand_tag = "apple"
                # ===================

                result_str += f"\n    [status_text]↳[/status_text] [{brand_tag}]{service}[/{brand_tag}] [status_text]\\[{country_str}][/status_text]"

        return result_str