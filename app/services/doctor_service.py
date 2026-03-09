from app.services import *
from app.models import Doctor
from bot.models import Region
from django.db.models import Q
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat

@sync_to_async
def filter_doctors_by_name_and_workplace(target, regions, fillial):
    query = Doctor.objects.filter(
        Q(Q(name__icontains = target) | Q(workplace__icontains = target)), 
        region__in = regions, fillial=fillial
        ).annotate(title=Concat(F('name'), Value(' | '), F('workplace'), output_field=CharField())).values()
    return query

async def get_doctor_by_id(id) -> Doctor:
    obj = await Doctor.objects.aget(id = id)
    return obj