# Generated by Django 4.1.6 on 2023-10-26 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.IntegerField(blank=True, choices=[(1, 'teacher'), (2, 'admin'), (3, 'reception'), (4, 'student')], null=True),
        ),
    ]
