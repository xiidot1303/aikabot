from app.views import *
from openpyxl import Workbook
from django.contrib import messages
from app.services.visit_service import visits_all

async def export_visits_view(request):
    # Создаем новый Excel файл
    wb = Workbook()
    ws = wb.active
    ws.title = "Посещения"

    # Записываем заголовки
    ws.append(["Пользователь", "Местоположение", "Комментария", "Дата", "Тип визита", "Расположение"])

    # Записываем данные
    async for visit in visits_all():
        ws.append([
            (await visit.get_bot_user()).name, visit.address, visit.comment, 
            visit.datetime.strftime("%d.%m.%Y %H:%M"), visit.get_type_display(), visit.location
            ])

    # Подготавливаем HTTP ответ с Excel файлом
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=visits.xlsx'
    wb.save(response)
    return response