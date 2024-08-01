from bot.bot import *
from app.services.visit_service import VISIT_TYPE
from app.services.doctor_service import filter_doctors_by_name
from app.services.pharmacy_service import filter_pharmacies_by_title
from app.services.partner_service import filter_partners_by_name

async def get_visit_address(update: Update, context: CustomContext):
    chat_id = update.effective_user.id
    text = update.inline_query.query
    bot_user: Bot_user = await get_user_by_update(update)
    # get visit_type from user data
    visit_type = context.user_data['visit_type']
    # set values list and decription attribute
    match visit_type:
        case VISIT_TYPE.doctor:
            values_list = await filter_doctors_by_name(text, await bot_user.get_region())
            title_attr = 'name'
            desc_attr = 'workplace'
        case VISIT_TYPE.pharmacy:
            values_list = await filter_pharmacies_by_title(text, await bot_user.get_region())
            title_attr = 'title'
            desc_attr = 'address'
        case VISIT_TYPE.partners:
            values_list = await filter_partners_by_name(text)
            title_attr = 'name'
            desc_attr = None

    # create inline query
    article = [
        await inlinequeryresultarticle(
            obj[title_attr],
            obj[desc_attr] if desc_attr else None,
            title_id=obj['id']
            ) 
            async for obj in values_list
    ]
    if not article:
        article = [
            await inlinequeryresultarticle(await get_word('not found', chat_id=update.inline_query.from_user.id))
        ]
    
    await update_inline_query_answer(update, article)