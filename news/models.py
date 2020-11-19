from django.db import models

import uuid
import os

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('news', filename)

class News(models.Model):
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=255,
        default='Заголовок'
    )

    file = models.FileField(
        verbose_name='Файл',
        upload_to=get_file_path,
        null=True,
        default=None
    )

    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        default=''
    )

    def __str__(self) -> str:
        return f'{self.title}'