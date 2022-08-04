# Generated by Django 4.1 on 2022-08-04 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Musics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('music_name', models.CharField(max_length=255)),
                ('artist', models.CharField(max_length=255)),
                ('genero', models.CharField(max_length=100)),
                ('path', models.CharField(max_length=255)),
                ('duration', models.FloatField()),
                ('liked', models.BooleanField()),
            ],
            options={
                'db_table': 'Musics',
                'managed': False,
            },
        ),
    ]
