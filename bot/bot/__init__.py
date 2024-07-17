from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes, CallbackContext, ExtBot, Application
from dataclasses import dataclass
from asgiref.sync import sync_to_async
from bot.utils import *
from bot.utils.bot_functions import *
from bot.utils.keyboards import *
from bot.resources.strings import lang_dict
from bot.services import *
from bot.services.language_service import *
from bot.services.string_service import *
from bot.resources.conversationList import *
from app.services import filter_objects_sync
from config import WEBAPP_URL

@dataclass
class WebhookUpdate:
    """Simple dataclass to wrap a custom update type"""
    user_id: int
    payload: str

class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    @classmethod
    def from_update(
        cls,
        update: object,
        application: "Application",
    ) -> "CustomContext":
        if isinstance(update, WebhookUpdate):
            return cls(application=application, user_id=update.user_id)
        return super().from_update(update, application)


async def is_message_back(update: Update):
    if update.message.text == await get_word("back", update):
        return True
    else:
        return False

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    bot = context.bot
    keyboards = [
        [await get_word('create visit', update)],
        # [await get_word('visit to the pharmacy', update)],
        # [await get_word('meeting with partners', update)],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True)
    await bot.send_message(
        update.effective_user.id
        await get_word('main menu', update),
        reply_markup=reply_markup
    )

    await check_username(update)

def check_user(func):
    async def wrapper(update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        if await is_staff_exists(user_id):
            # "User is accessed to use bot"
            return await func(update, context)
        else:
            # User is restricted to use bot
            text = "Вам отказано в доступе"
            await update.message.reply_text(text)
            return ConversationHandler.END
    return wrapper