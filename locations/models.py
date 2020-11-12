from django.db import models


class Region(models.Model):
    code = models.PositiveIntegerField(
        verbose_name = 'Код региона',
        unique = True,
    )
    name = models.CharField(
        verbose_name = 'Название региона',
        max_length = 50,
    )

    def __str__(self):
        return f'{self.code} - {self.name}'
    

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
    

class City(models.Model):
    code = models.PositiveIntegerField(
        verbose_name = 'Код города',
        unique = True,
    )

    name = models.CharField(
        verbose_name = 'Название города', 
        max_length = 255,
    )

    region = models.ForeignKey(
        Region, 
        verbose_name = 'Регион', 
        on_delete = models.PROTECT,
    )

    def __str__(self):
        return f'{self.code} - {self.name}'
    

    class Meta:
        unique_together = ('code', 'region')
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class School(models.Model):
    code = models.PositiveIntegerField(
        verbose_name = 'Код школы',
        unique = True,
    )

    name = models.TextField(
        verbose_name = 'Название школы', 
    )

    city = models.ForeignKey(
        City, 
        verbose_name = 'Город', 
        on_delete = models.PROTECT,
    )

    def __str__(self):
        return f'{self.code} - {self.name}'
    


    class Meta:
        unique_together = ('code', 'city')
        verbose_name = 'Школа'
        verbose_name_plural = 'Школы'