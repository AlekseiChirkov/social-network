# Generated by Django 3.2.5 on 2021-07-18 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]