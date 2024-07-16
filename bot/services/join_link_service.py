from app.services import *
from bot.models import JoinLink

async def create_join_link(link_, code):
    obj = await JoinLink.objects.acreate(link = link_, code = code)
    return obj

@sync_to_async
def get_unused_join_link_by_code(code):
    if query := JoinLink.objects.filter(code = code, is_used = False):
        return query[0]
    else:
        return None