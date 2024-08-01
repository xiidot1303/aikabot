from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    InlineQueryHandler,
    TypeHandler,
    ConversationHandler
)

from bot.resources.strings import lang_dict
from bot.resources.conversationList import *

from bot.bot import (
    main, login, visit, search
)

exceptions_for_filter_text = (~filters.COMMAND) & (~filters.Text(lang_dict['main menu']))

login_handler = ConversationHandler(
    entry_points=[CommandHandler("start", main.start)],
    states={
        GET_LANG: [
            MessageHandler(filters.Text(lang_dict["uz_ru"]), login.get_lang),
            MessageHandler(filters.TEXT & (~filters.COMMAND), login.get_lang)
        ],
        GET_NAME: [
            MessageHandler(filters.TEXT & (~filters.COMMAND), login.get_name)
        ],
        GET_CONTACT: [
            MessageHandler(filters.CONTACT, login.get_contact),
            MessageHandler(filters.Text(lang_dict['back']), login.get_contact),
            MessageHandler(filters.TEXT & (~filters.COMMAND), login.get_contact)
        ]
    },
    fallbacks=[
        CommandHandler("start", login.start)
    ],
    name="login",
    persistent=True
)

visit_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Text(lang_dict['create visit']), main.visit)
    ],
    states={
        GET_VISIT_TYPE: [
            MessageHandler(filters.TEXT & exceptions_for_filter_text, visit.get_visit_type)
        ],
        GET_VISIT_LOCATION: [
            MessageHandler(filters.LOCATION | filters.Text(lang_dict['back']), visit.get_location)
        ],
        GET_VISIT_ADRESS: [
            MessageHandler(filters.TEXT & exceptions_for_filter_text, visit.get_address),
        ],
        GET_VIDEO_NOTE: [
            MessageHandler(filters.VIDEO_NOTE | filters.Text(lang_dict['back']), visit.get_video_note),
        ],
        GET_VISIT_COMMENT: [
            MessageHandler(filters.TEXT & exceptions_for_filter_text, visit.get_comment)
        ],
        CONFIRM_VISIT: [
            MessageHandler(filters.Text(lang_dict['back']), visit._to_the_getting_comment),
            CallbackQueryHandler(visit.confirm_visit, pattern=r"^confirm_visit")
        ],

    },
    fallbacks=[
        CommandHandler("start", visit.start),
        MessageHandler(filters.Text(lang_dict['main menu']), visit.start)
    ],
    name="visit",
    persistent=True,
)

handlers = [
    login_handler,
    visit_handler,
    InlineQueryHandler(search.get_visit_address),
]