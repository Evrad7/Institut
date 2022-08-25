# Generated by Django 3.2.7 on 2009-01-01 00:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('direction', '0004_alter_professeur_numero_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='cc1',
            field=models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)], verbose_name='controle continu 1'),
        ),
        migrations.AlterField(
            model_name='note',
            name='cc2',
            field=models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)], verbose_name='controle continu 2'),
        ),
        migrations.AlterField(
            model_name='note',
            name='sn1',
            field=models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)], verbose_name='Session normale 1'),
        ),
        migrations.AlterField(
            model_name='note',
            name='sn2',
            field=models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)], verbose_name='Session normale 2'),
        ),
    ]
