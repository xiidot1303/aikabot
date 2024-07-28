from bot.bot import *
from app.services.visit_service import *
from app.services.doctor_service import *
from app.services.pharmacy_service import *
from app.services.partner_service import *
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
    visit_type = context.user_data['visit_type']
    match visit_type:
        case VISIT_TYPE.doctor:
            text = await get_word('select doctor or add', update)
            add_button_text = await get_word('add doctor', update)
            search_button_text = await get_word('select doctor', update)
        case VISIT_TYPE.pharmacy:
            text = await get_word('select pharmacy or add', update)
            add_button_text = await get_word('add pharmacy', update)
            search_button_text = await get_word('select pharmacy', update)
        case VISIT_TYPE.partners:
            text = await get_word('select partner or add', update)
            add_button_text = await get_word('add partner', update)
            search_button_text = await get_word('select partner', update)
        case _:
            return
    web_app_info = WebAppInfo(url=f"{WEBAPP_URL}/{visit_type}-add")
    i_buttons = [
        [InlineKeyboardButton(text=search_button_text, switch_inline_query_current_chat="")],
        [InlineKeyboardButton(text=add_button_text, web_app=web_app_info)]
    ]
    
    markup = InlineKeyboardMarkup(i_buttons)
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
        type = VISIT_TYPE.doctor
    elif visit_type == await get_word('visit to the pharmacy', update):
        type = VISIT_TYPE.pharmacy
    elif visit_type == await get_word('meeting with partners', update):
        type = VISIT_TYPE.partners
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

    address, address_id = await split_text_and_text_id(update.message.text)
    visit_type = context.user_data['visit_type']
    match visit_type:
        case VISIT_TYPE.doctor:
            doctor: Doctor = await get_doctor_by_id(address_id)
            context.user_data['doctor_id'] = doctor.id
        case VISIT_TYPE.pharmacy:
            pharmacy: Pharmacy = await get_pharmacy_by_id(address_id)
            context.user_data['pharmacy_id'] = pharmacy.id
        case VISIT_TYPE.partners:
            partner: Partner = await get_partner_by_id(address_id)
            context.user_data['partner_id'] = partner.id

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
    comment = context.user_data['comment']
    visit_type = context.user_data['visit_type']
    lat, lon = context.user_data['lat'], context.user_data['lon']
    doctor, pharmacy, partner = (None, None, None)
    match visit_type:
        case VISIT_TYPE.doctor:
            doctor_id = context.user_data['doctor_id']
            doctor: Doctor = await get_doctor_by_id(doctor_id)
        case VISIT_TYPE.pharmacy:
            pharmacy_id = context.user_data['pharmacy_id']
            pharmacy: Pharmacy = await get_pharmacy_by_id(pharmacy_id)
        case VISIT_TYPE.partners:
            partner_id = context.user_data['partner_id']
            partner: Partner = await get_partner_by_id(partner_id)
    # create visit address object
    address: VisitAdress = await create_visit_address(doctor, pharmacy, partner)
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