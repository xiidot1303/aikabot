from django.urls import path, re_path
from config import BOT_API_TOKEN
from django.conf import settings
from django.conf.urls.static import static
from config import DEBUG
from bot.views import botwebhook, join_link

urlpatterns = [
    path(BOT_API_TOKEN, botwebhook.BotWebhookView.as_view()),

    # join link
    path('join-link-create', join_link.create, name="create_join_link")
]

if DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)