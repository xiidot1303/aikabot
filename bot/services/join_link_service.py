from app.services import *
from bot.models import JoinLink

async def create_join_link(link_):
    obj = await JoinLink.objects.acreate(link = link_)
    return obj