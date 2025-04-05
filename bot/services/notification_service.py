from bot.bot import *
from app.models import Visit
from bot.models import Bot_user, Fillial
from config import REPORT_GROUP_ID

async def send_visit_summary_notify(visit: Visit):
    bot_user: Bot_user = await visit.get_bot_user()
    fillial: Fillial = await bot_user.get_fillial
    text = await new_visit_info_string(visit)
    await send_newsletter(bot, fillial.tg_id, text)
    await bot.send_video_note(fillial.tg_id, visit.video_note)