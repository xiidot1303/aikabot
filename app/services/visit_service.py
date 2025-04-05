from app.services import *
from app.models import Visit, VisitAdress
from django.utils import timezone

class VISIT_TYPE:
    doctor = "doctor"
    pharmacy = "pharmacy"
    partners = "partners"

async def create_visit(bot_user, address, comment, type, lat, lon, video, video_note) -> Visit:
    obj = await Visit.objects.acreate(
        bot_user = bot_user, address = address,
        comment = comment, type = type, lat = lat, lon = lon,
        video = video, video_note = video_note
    )
    return obj

async def create_visit_address(doctor, pharmacy, partner):
    obj = await VisitAdress.objects.acreate(doctor = doctor, pharmacy = pharmacy, partner = partner)
    return obj

async def get_visit_by_id(id):
    obj = await Visit.objects.aget(id = id)
    return obj

def filter_visits_by_date_range(start_date, end_date, fillial):
    # create start date obj
    date_obj = datetime.strptime(start_date, "%d.%m.%Y")
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    start_date = timezone.datetime(year, month, day)
    # create end date obj
    date_obj = datetime.strptime(end_date, "%d.%m.%Y")
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    end_date = timezone.datetime(year, month, day, 23, 59)
    query = Visit.objects.filter(datetime__gte=start_date, datetime__lte=end_date)
    if fillial:
        query = query.filter(bot_user__fillial_id=fillial)
    return query 