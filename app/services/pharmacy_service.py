from app.services import *
from app.models import Pharmacy
from bot.models import Region

@sync_to_async
def filter_pharmacies_by_title(title, regions, fillial):
    query = Pharmacy.objects.filter(title__icontains = title, region__in=regions, fillial=fillial).values()
    return query

async def get_pharmacy_by_id(id) -> Pharmacy:
    obj = await Pharmacy.objects.aget(id = id)
    return obj