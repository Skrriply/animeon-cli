from dataclasses import dataclass


@dataclass(slots=True)
class AnimePreview:
    """
    Anime preview model.

    Attributes:
        text_content: Preview text content.
        poster_path: Path to poster image.
    """

    text_content: str
    poster_path: str  # Optional[str]

    def to_dict(self):
        return {"text_content": self.text_content, "poster_path": self.poster_path}
