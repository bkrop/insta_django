# Generated by Django 3.1.1 on 2020-10-14 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20201010_1253'),
        ('posts', '0003_hashtag'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(related_name='posts', to='users.Profile'),
        ),
    ]
