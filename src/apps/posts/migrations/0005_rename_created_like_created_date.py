# Generated by Django 3.2.5 on 2021-07-19 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20210718_0908'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='created',
            new_name='created_date',
        ),
    ]