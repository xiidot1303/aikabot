from app.services import *
from app.models import Doctor
from bot.models import Region

@sync_to_async
def filter_doctors_by_name(name, regions):
    query = Doctor.objects.filter(name__icontains = name, region__in = regions).values()
    return query

async def get_doctor_by_id(id) -> Doctor:
    obj = await Doctor.objects.aget(id = id)
    return obj