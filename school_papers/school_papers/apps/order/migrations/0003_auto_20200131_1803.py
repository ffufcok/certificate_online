# Generated by Django 3.0.2 on 2020-01-31 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20200111_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email'),
        ),
    ]
