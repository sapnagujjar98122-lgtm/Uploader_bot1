import asyncio
import logging
from datetime import datetime
from utils.scraper import get_anime
from config import Config

logger = logging.getLogger(__name__)

class AutoUploadChecker:
    def __init__(self, app, db, queue_mgr):
        self.app = app
        self.db  = db
        self.q   = queue_mgr

    async def start(self):
        logger.info("Auto-check scheduler started.")
        while True:
            interval = (await self.db.get("auto_check_interval")
                        or Config.AUTO_CHECK_INTERVAL)
            await asyncio.sleep(interval * 60)
            await self._check_all()

    async def _check_all(self):
        tracks = await self.db.get_tracks()
        if not tracks:
            return
        logger.info(f"Auto-checking {len(tracks)} tracked anime…")
        for track in tracks:
            try:
                await self._check_one(track)
            except Exception as e:
                logger.error(f"Auto-check error for {track.get('name')}: {e}")

    async def _check_one(self, track: dict):
        detail = await get_anime(track["aid"])
        if not detail:
            return

        # Find the correct season entry
        seasons = detail.get("seasons", [])
        season_data = next(
            (s for s in seasons if s["num"] == track["season"]), None
        )
        if not season_data:
            return

        # Get next airing ep
        next_ep = detail.get("next_ep")
        current_ep = season_data.get("episodes", 0)

        # Compare with what we last uploaded
        last_ep = track.get("last_ep", 0)

        # Notify admins if new episode is out
        if current_ep and current_ep > last_ep:
            new_ep = last_ep + 1
            msg = (
                f"🆕 <b>New Episode Alert!</b>\n\n"
                f"📺 <b>{detail['title']}</b>\n"
                f"📌 Season {track['season']:02d} | Episode {new_ep:02d} is available!\n\n"
                f"Use /upload {detail['title']} to upload it.\n"
                f"Or use /auto_upload to configure auto-fetching."
            )
            for aid in await self.db.get_admins():
                try:
                    await self.app.send_message(aid, msg, parse_mode="html")
                except Exception:
                    pass

        elif next_ep:
            airing_ts = next_ep.get("airingAt", 0)
            ep_num    = next_ep.get("episode", "?")
            airing_dt = datetime.utcfromtimestamp(airing_ts).strftime("%Y-%m-%d %H:%M UTC") if airing_ts else "?"
            logger.info(
                f"{detail['title']} S{track['season']} next ep={ep_num} "
                f"airs at {airing_dt}"
            )
