# Generated by Django 3.2 on 2022-06-09 11:22

from django.db import migrations, models
from django.contrib.auth.models import Group


def create_groups(apps, schema_editor):
    admin_group, _ = Group.objects.get_or_create(name='Administrator')
    facility_admin_group, _ = Group.objects.get_or_create(name='Facility Admin')
    teacher_group, _ = Group.objects.get_or_create(name='Teacher')
    parent_group, _ = Group.objects.get_or_create(name='Parent')


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programme', models.CharField(max_length=100, null=True)),
                ('gender', models.CharField(max_length=100, null=True)),
                ('enrollment_year', models.IntegerField(max_length=100, null=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('phone_number', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
                ('completion_year', models.IntegerField(max_length=100, null=True)),
            ],
        ),
    ]
