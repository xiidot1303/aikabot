from bot.bot import *
from app.services.visit_service import *
from app.services.visit_service import *
import asyncio
from app.utils import get_address_by_coordinates

async def _to_the_getting_visit_type(update: Update, context: CustomContext):
    buttons = [
        await get_word('visit to the doctor', update),
        await get_word('visit to the pharmacy', update),
        await get_word('meeting with partners', update),
    ]
    markup = await build_keyboard(update, buttons, 1, back_button=False)
    text = await get_word('select type of visit', update)
    await update_message_reply_text(update, text, reply_markup=markup)
    return GET_VISIT_TYPE

async def _to_the_getting_location(update: Update, context: CustomContext):
    text = await get_word('send live location', update)
    markup = await build_keyboard(update, [], 2)
    await update_message_reply_text(update, text, markup)
    return GET_VISIT_LOCATION

async def _to_the_getting_address(update: Update, context: CustomContext):
    markup = await build_keyboard(update, [], 2)
    text = await get_word('type address', update)
    await update_message_reply_text(update, text, reply_markup=markup)
    return GET_VISIT_ADRESS

async def _to_the_getting_comment(update: Update, context: CustomContext):
    markup = await build_keyboard(update, [], 2)
    text = await get_word('type comment', update)
    await update_message_reply_text(update, text, reply_markup=markup)
    return GET_VISIT_COMMENT


async def _to_the_confirming_visit(update: Update, context: CustomContext):
    text = await confirm_visit_string(update, context.user_data)
    i_buttons = [[
        InlineKeyboardButton(text=await get_word('yes', update), callback_data='confirm_visit-yes'),
        InlineKeyboardButton(text=await get_word('no', update), callback_data='confirm_visit-no'),
    ]]
    markup = InlineKeyboardMarkup(i_buttons)
    await update_message_reply_text(update, text, reply_markup=markup)
    return CONFIRM_VISIT

################################################################################################
################################################################################################

@check_user
async def get_visit_type(update: Update, context: CustomContext):
    visit_type = update.message.text
    if visit_type == await get_word('visit to the doctor', update):
        type = 'doctor'
    elif visit_type == await get_word('visit to the pharmacy', update):
        type = 'pharmacy'
    elif visit_type == await get_word('meeting with partners', update):
        type = 'partners'
    else:
        return
    
    context.user_data['visit_type'] = type
    return await _to_the_getting_location(update, context)

@check_user
async def get_location(update: Update, context: CustomContext):
    if await is_message_back(update):
        return await _to_the_getting_visit_type(update, context)
    message = update.message if update.message else update.edited_message
    if message.location.live_period:
        lat = message.location.latitude
        lon = message.location.longitude
        # get driver by update
        context.user_data['lat'] = lat
        context.user_data['lon'] = lon
        return await _to_the_getting_address(update, context)
    return

@check_user
async def get_address(update: Update, context: CustomContext):
    if await is_message_back(update):
        return await _to_the_getting_location(update, context)

    address = update.message.text
    context.user_data['address'] = address
    return await _to_the_getting_comment(update, context)

@check_user
async def get_comment(update: Update, context: CustomContext):
    if await is_message_back(update):
        return await _to_the_getting_address(update, context)
    
    comment = update.message.text
    context.user_data['comment'] = comment
    return await _to_the_confirming_visit(update, context)

@check_user
async def confirm_visit(update: Update, context: CustomContext):
    query: CallbackQuery = update.callback_query
    data = query.data
    *args, answer = str(data).split('-')
    if answer == 'yes':
        text = await get_word('visit is completed', update)
        await bot_send_message(update, context, text, reply_markup=ReplyKeyboardRemove(True))
    else:
        text = await get_word('visit is canceled', update)
        await bot_send_message(update, context, text, reply_markup=ReplyKeyboardRemove(True))
    
    # get all attributes
    bot_user = await get_user_by_update(update)
    address = context.user_data['address']
    comment = context.user_data['comment']
    visit_type = context.user_data['visit_type']
    lat, lon = context.user_data['lat'], context.user_data['lon']
    # create visit object
    visit_obj: Visit = await create_visit(bot_user, address, comment, visit_type, lat, lon)
    # set address to Visit by lat and lon
    context.job_queue.run_once(set_location_of_visit, 0, data=(lat,lon, visit_obj.id), chat_id=update.effective_message.chat_id)

    await update.callback_query.edit_message_reply_markup(reply_markup=None)
    await main_menu(update, context)
    return ConversationHandler.END

async def set_location_of_visit(context: CustomContext):
    job = context.job
    lat, lon, visit_id = job.data
    visit: Visit = await get_visit_by_id(visit_id)
    address = await get_address_by_coordinates(lat, lon)
    visit.location = address
    await visit.asave()

async def start(update: Update, context: CustomContext):
    await main_menu(update, context)
    return ConversationHandler.END