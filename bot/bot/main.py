from bot.bot import *
from bot.services.join_link_service import *
from bot.bot.visit import _to_the_getting_visit_type
import json
import logging
import traceback
import html

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

logger = logging.getLogger(__name__)

async def error_handler(update: Update, context: CustomContext):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(
        chat_id=206261493, text=message, parse_mode=ParseMode.HTML
    )