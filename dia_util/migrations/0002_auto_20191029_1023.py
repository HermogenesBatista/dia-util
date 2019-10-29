# Generated by Django 2.1 on 2019-10-29 10:23

from django.db import migrations

from ..Bd.bd import DADOS_FERIADOS


def insert_some_holidays(apps, schema_editor):
    Holiday = apps.get_model("dia_util", "Holiday")
    list_of_holidays = [
        Holiday(
            date=x[1],
            description=x[2]
        ) for x in DADOS_FERIADOS
    ]
    Holiday.objects.bulk_create(list_of_holidays)


class Migration(migrations.Migration):

    dependencies = [
        ('dia_util', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_some_holidays),
    ]