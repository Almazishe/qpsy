from django.db import models

from bot.models import TelegramUser

SENT = 'TO'
RECEIVED= 'FROM'

TO_FROM = (
    (SENT, 'SENT'),
    (RECEIVED, 'RECEIVED'),
)


class Message(models.Model):
    tg_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    text  = models.TextField()

    status = models.CharField(
        choices=TO_FROM,
        max_length=10,
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self) -> str:
        return f'{self.tg_user.name}'
