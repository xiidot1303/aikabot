from app.models import Visit

async def create_visit(bot_user, address, comment, type, lat, lon) -> Visit:
    obj = await Visit.objects.acreate(
        bot_user = bot_user, address = address,
        comment = comment, type = type, lat = lat, lon = lon
    )
    return obj

async def get_visit_by_id(id):
    obj = await Visit.objects.aget(id = id)
    return obj