# Generated by Django 3.2.7 on 2009-01-01 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('direction', '0011_alter_absenceetudiant_etudiant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absenceprofesseur',
            name='heure_debut',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='absenceprofesseur',
            name='heure_fin',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='absenceprofesseur',
            name='motif',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
