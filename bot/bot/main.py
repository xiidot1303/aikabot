from bot.bot import *
from bot.services.join_link_service import *
from bot.bot.visit import _to_the_getting_visit_type

async def start(update: Update, context: CustomContext):
    if await is_group(update):
        return
    
    if await is_staff_exists(update.message.chat.id):
        # main menu
        await main_menu(update, context)
        return
    else:
        start_msg = await get_start_msg(update.message.text)
        if start_msg:
            # get active join link by start msg
            join_link: JoinLink = await get_unused_join_link_by_code(start_msg)
            if join_link:
                # set join link objects as used
                bot_user: Bot_user = await get_or_create(user_id=update.message.chat_id)
                # activate bot user
                bot_user.is_active = True
                await  bot_user.asave()
                join_link.bot_user = bot_user
                join_link.is_used = True
                join_link.used_date = await datetime_now()
                await join_link.asave()
                # send message to select lang
                hello_text = lang_dict['hello']
                await update_message_reply_text(
                    update,
                    hello_text,
                    reply_markup= await select_lang_keyboard()
                )
                return GET_LANG

        # User is restricted to use bot
        text = "Вам отказано в доступе"
        await update.message.reply_text(text)
        return

@check_user
async def visit(update: Update, context: CustomContext):
    return await _to_the_getting_visit_type(update, context)