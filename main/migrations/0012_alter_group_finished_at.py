# Generated by Django 4.1.6 on 2023-10-31 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_group_finished_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='finished_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]