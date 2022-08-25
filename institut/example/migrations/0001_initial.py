# Generated by Django 3.2.7 on 2008-12-31 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jeu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
                ('type', models.CharField(max_length=30)),
                ('taille', models.CharField(max_length=10)),
                ('prix', models.PositiveIntegerField()),
            ],
        ),
    ]
