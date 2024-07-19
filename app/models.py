from django.db import models
from asgiref.sync import sync_to_async

class Visit(models.Model):
    bot_user = models.ForeignKey('bot.Bot_user', null=True, blank=False, on_delete=models.PROTECT, verbose_name="Пользователь")
    address = models.CharField(null=True, blank=True, max_length=255, verbose_name="Местоположение")
    comment = models.TextField(null=True, blank=True, max_length=1024, verbose_name="Комментария")
    datetime = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True, verbose_name='Дата')
    TYPE_CHOICES = [
        ('doctor', 'Визит к врачу'),
        ('pharmacy', 'Визит в аптеку'),
        ('partners', 'Встреча с партнерами'),
    ]
    type = models.CharField(null=True, blank=False, max_length=32, choices=TYPE_CHOICES, verbose_name="Тип визита")
    lat = models.CharField(null=True, blank=True, max_length=16)
    lon = models.CharField(null=True, blank=True, max_length=16)
    location = models.CharField(null=True, blank=True, max_length=255, verbose_name='Расположение')
    
    @sync_to_async
    def get_bot_user(self):
        return self.bot_user
    
    class Meta:
        verbose_name = "Посещение"
        verbose_name_plural = "Посещения"
    
class Doctor(models.Model):
    name = models.CharField(null=True, blank=False, max_length=255, verbose_name="Имя")
    workplace = models.CharField(null=True, blank=True, max_length=255, verbose_name="Место работы")

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"


class Pharmacy(models.Model):
    title = models.CharField(null=True, blank=False, max_length=255, verbose_name="Название")
    address = models.CharField(null=True, blank=True, max_length=255, verbose_name="Адрес")

    class Meta:
        verbose_name = "Аптека"
        verbose_name_plural = "Аптеки"