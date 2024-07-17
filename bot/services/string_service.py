from bot.services.language_service import *

async def confirm_visit_string(update, data):
    address, comment = data['address'], data['comment']
    text = f"{await get_word('address', update)}: <b>{address}</b>\n" \
        f"{await get_word('comment', update)}; <b>{comment}</b>\n\n" \
            f"<i>{await get_word('confirm visit?', update)}</i>"
    return text