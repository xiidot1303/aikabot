from django.db import models
from django.core.validators import FileExtensionValidator
from asgiref.sync import sync_to_async

class Bot_user(models.Model):
    user_id = models.BigIntegerField(null=True)
    name = models.CharField(null=True, blank=True, max_length=256, default='', verbose_name='Имя')
    username = models.CharField(null=True, blank=True, max_length=256, verbose_name='username')
    firstname = models.CharField(null=True, blank=True, max_length=256, verbose_name='Никнейм')
    phone = models.CharField(null=True, blank=True, max_length=16, default='', verbose_name='Телефон')
    lang = models.CharField(null=True, blank=True, max_length=4, default='uz', verbose_name='')
    date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True, verbose_name='Дата регистрации')
    regions = models.ManyToManyField('bot.Region', verbose_name='Район')
    is_active = models.BooleanField(default=True, verbose_name='Активен?')

    def __str__(self) -> str:
        try:
            return self.name + ' ' + str(self.phone)
        except:
            return super().__str__()

    @sync_to_async
    def get_regions(self):
        return self.regions.all()

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"
    
class Message(models.Model):
    bot_users = models.ManyToManyField('bot.Bot_user', blank=True, related_name='bot_users_list', verbose_name='Пользователи бота')
    text = models.TextField(null=True, blank=False, max_length=1024, verbose_name='Текст')
    photo = models.FileField(null=True, blank=True, upload_to="message/photo/", verbose_name='Фото',
        validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','bmp','gif'])]
    )
    video = models.FileField(
        null=True, blank=True, upload_to="message/video/", verbose_name='Видео',
        validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])]
        )
    file = models.FileField(null=True, blank=True, upload_to="message/file/", verbose_name='Файл')
    is_sent = models.BooleanField(default=False)
    date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True, verbose_name='Дата')

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
    
class JoinLink(models.Model):
    bot_user = models.ForeignKey('bot.Bot_user', blank=True, null=True, verbose_name='Пользователь', on_delete=models.PROTECT)
    link = models.CharField(null=True, blank=True, max_length=255, verbose_name='Ссылка')
    code = models.CharField(null=True, blank=True, max_length=64, verbose_name='Код')
    is_used = models.BooleanField(default=False, verbose_name="Использован?")
    used_date = models.DateTimeField(null=True, blank=True, verbose_name = "Дата использования")

    class Meta:
        verbose_name = "Ссылка на приглашение"
        verbose_name_plural = "Ссылки для приглашений"

class Region(models.Model):
    title = models.CharField(null=True, blank=False, max_length=255, verbose_name='Название региона')

    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Районы"
    
    def __str__(self) -> str:
        return self.title