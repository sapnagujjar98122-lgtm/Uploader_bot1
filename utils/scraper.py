import aiohttp
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)
ANILIST = "https://graphql.anilist.co"

_SEARCH_QUERY = """
query ($q: String) {
  Page(perPage: 6) {
    media(search: $q, type: ANIME, sort: SEARCH_MATCH) {
      id
      title { romaji english }
      episodes
      status
      seasonYear
      genres
      averageScore
      coverImage { large }
      nextAiringEpisode { episode airingAt }
    }
  }
}
"""

_DETAIL_QUERY = """
query ($id: Int) {
  Media(id: $id, type: ANIME) {
    id
    title { romaji english }
    episodes
    status
    seasonYear
    coverImage { large }
    nextAiringEpisode { episode airingAt }
    relations {
      edges {
        relationType
        node { id title { romaji english } type episodes seasonYear }
      }
    }
  }
}
"""

async def _gql(query: str, variables: dict) -> Optional[dict]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                ANILIST,
                json={"query": query, "variables": variables},
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=15)
            ) as r:
                return await r.json()
    except Exception as e:
        logger.error(f"AniList request failed: {e}")
        return None

def _title(media: dict) -> str:
    return media["title"]["english"] or media["title"]["romaji"]

async def search_anime(query: str) -> List[Dict]:
    data = await _gql(_SEARCH_QUERY, {"q": query})
    if not data:
        return []
    results = []
    for m in data.get("data", {}).get("Page", {}).get("media", []):
        results.append({
            "id":       m["id"],
            "title":    _title(m),
            "romaji":   m["title"]["romaji"],
            "episodes": m.get("episodes") or "?",
            "status":   m.get("status", ""),
            "year":     m.get("seasonYear"),
            "cover":    m.get("coverImage", {}).get("large"),
            "score":    m.get("averageScore"),
            "next_ep":  m.get("nextAiringEpisode"),
        })
    return results

async def get_anime(anime_id: int) -> Optional[Dict]:
    data = await _gql(_DETAIL_QUERY, {"id": anime_id})
    if not data:
        return None
    m = data.get("data", {}).get("Media")
    if not m:
        return None

    # Build season list (main + sequels)
    seasons = [{"id": m["id"], "num": 1, "title": _title(m),
                "episodes": m.get("episodes") or 0}]
    snum = 2
    for edge in m.get("relations", {}).get("edges", []):
        if (edge["relationType"] == "SEQUEL"
                and edge["node"]["type"] == "ANIME"):
            n = edge["node"]
            seasons.append({
                "id":       n["id"],
                "num":      snum,
                "title":    _title(n),
                "episodes": n.get("episodes") or 0,
            })
            snum += 1

    return {
        "id":       m["id"],
        "title":    _title(m),
        "episodes": m.get("episodes") or 0,
        "status":   m.get("status"),
        "cover":    m.get("coverImage", {}).get("large"),
        "next_ep":  m.get("nextAiringEpisode"),
        "seasons":  seasons,
    }
