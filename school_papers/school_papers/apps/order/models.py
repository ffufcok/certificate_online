from django.db import models


class Info(models.Model):
    surname = models.CharField('фамилия', max_length=50)
    name = models.CharField('имя', max_length=50)
    father = models.CharField('отчество', max_length=50)
    class_letter = models.CharField('класс', max_length=50)
    email = models.CharField('email', max_length=50)
    date = models.DateTimeField('дата заявки')
    confirmation = models.IntegerField('подтверждение', default=0)

    class Meta:
        verbose_name = 'Информацию об ученике'
        verbose_name_plural = 'Информация об ученике'
