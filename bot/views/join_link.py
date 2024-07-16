from app.views import *
from app.utils import generate_random_symbols
from bot.control.updater import application
from bot.services.join_link_service import create_join_link

async def create(request):
    if request.method == 'POST':
        number_of_links = int(request.POST.get('number_of_link', 1))
        bot_data = await application.bot.get_me()
        bot_name = bot_data.username
        for i in range(number_of_links):
            random_symbol = await generate_random_symbols(10)
            link_ = f"t.me/{bot_name}?start={random_symbol}"
            join_link = await create_join_link(link_, random_symbol)
        messages.success(request, f'Успешно создано {number_of_links} ссылок')
    return redirect("admin:bot_joinlink_changelist")
