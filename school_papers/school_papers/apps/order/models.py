from django.db import models


class Info(models.Model):
    surname = models.CharField('фамилия', max_length=50)
    name = models.CharField('имя', max_length=50)
    father = models.CharField('отчество', max_length=50)
    class_letter = models.CharField('класс', max_length=50)
    email = models.EmailField('email')
    date = models.DateTimeField('дата заявки')
    confirmation = models.IntegerField('подтверждение', default=0)

    class Meta:
        verbose_name = 'Информацию об ученике'
        verbose_name_plural = 'Информация об ученике'


class Schools(models.Model):
    name = models.CharField('Название школы', max_length=50)
    email = models.EmailField('Электронная почта секретаря', max_length=50)

    class Meta:
        verbose_name = 'Информацию о школе'
        verbose_name_plural = 'Информация о школе'
