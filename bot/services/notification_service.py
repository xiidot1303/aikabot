from bot.bot import *
from app.models import Visit
from config import REPORT_GROUP_ID

async def send_visit_summary_notify(visit: Visit):
    text = await new_visit_info_string(visit)
    await send_newsletter(bot, REPORT_GROUP_ID, text)
    await bot.send_video_note(REPORT_GROUP_ID, visit.video_note)