import re
from config import Config

VARIABLES = {
    "{anime_name}", "{season}", "{episode}", "{audio}", "{quality}"
}

def format_caption(template: str, **kwargs) -> str:
    """Fill caption template with given values."""
    result = template
    for k, v in kwargs.items():
        result = result.replace("{" + k + "}", str(v))
    return result

def validate_template(template: str) -> bool:
    """Check template has no unknown vars."""
    found = set(re.findall(r"\{[^}]+\}", template))
    return found.issubset(VARIABLES)

def build_caption(
    template: str,
    anime_name: str,
    season: int,
    episode: int,
    audio: str,
    quality: str,
) -> str:
    s = f"Season {season:02d}"
    e = f"Episode {episode:02d}"
    return format_caption(template,
        anime_name=anime_name,
        season=s, episode=e,
        audio=audio, quality=quality)
  
