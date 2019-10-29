# Generated by Django 2.1 on 2019-10-29 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Holiday',
                'verbose_name': 'Holiday',
                'verbose_name_plural': 'Holidays',
            },
        ),
    ]
