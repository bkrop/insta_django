# Generated by Django 3.1.1 on 2020-10-10 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201010_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='follow',
            field=models.ManyToManyField(blank=True, null=True, related_name='_profile_follow_+', to='users.Profile'),
        ),
    ]
