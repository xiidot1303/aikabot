from app.services import *
from app.models import Doctor

@sync_to_async
def filter_doctors_by_name(name):
    query = Doctor.objects.filter(name__icontains = name).values()
    return query

async def get_doctor_by_id(id) -> Doctor:
    obj = await Doctor.objects.aget(id = id)
    return obj