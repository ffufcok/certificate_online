from django.db import models


class Info(models.Model):
    surname = models.CharField('фамилия', max_length=50)
    name = models.CharField('имя', max_length=50)
    father = models.CharField('отчество', max_length=50)
    class_letter = models.CharField('класс', max_length=50)
    email = models.EmailField('email')
    date = models.DateTimeField('дата заявки')
    confirmation = models.IntegerField('потверждение', default=0)
    schools = models.CharField('школа', max_length=50, default='НЕИЗВЕСТНО')

    class Meta:
        verbose_name = 'Информацию об ученике'
        verbose_name_plural = 'Информация об ученике'


class Schools(models.Model):
    name = models.CharField('Название школы', max_length=50)
    email = models.EmailField('Электронная почта секретаря', max_length=50)
    name_in_english = models.CharField('Название школы на английской языке', max_length=50, default='НЕИЗВЕСТНО')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Информацию о школе'
        verbose_name_plural = 'Информация о школе'
