from app.services import *
from app.models import Pharmacy

@sync_to_async
def filter_pharmacies_by_title(title):
    query = Pharmacy.objects.filter(title__icontains = title).values()
    return query

async def get_pharmacy_by_id(id) -> Pharmacy:
    obj = await Pharmacy.objects.aget(id = id)
    return obj