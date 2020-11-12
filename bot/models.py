from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

class TelegramUser(models.Model):
    chat_id = models.PositiveIntegerField(
        verbose_name = 'Код чата',
        unique = True,
    )

    name = models.CharField(
        verbose_name = 'Псевдоним',
        max_length = 255,
        default = 'Друг'
    )


    main_psy = models.ForeignKey(
        User,
        verbose_name = 'Основной психолог',
        on_delete = models.PROTECT,
        related_name = 'main_students'
    )

    active_psy = models.ForeignKey(
        User,
        verbose_name = 'Текущий психолог',
        on_delete = models.PROTECT,
        related_name = 'active_students'
    )

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
