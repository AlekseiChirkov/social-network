# Generated by Django 3.2.5 on 2021-07-19 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_rename_created_like_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='created_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
