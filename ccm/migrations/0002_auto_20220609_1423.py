# Generated by Django 3.2 on 2022-06-09 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='completion_year',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='enrollment_year',
            field=models.IntegerField(null=True),
        ),
    ]
