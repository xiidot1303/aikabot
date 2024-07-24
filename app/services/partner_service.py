from app.services import *
from app.models import Partner

@sync_to_async
def filter_partners_by_name(name):
    query = Partner.objects.filter(name__icontains = name).values()
    return query

async def get_partner_by_id(id):
    obj = await Partner.objects.aget(id = id)
    return obj