# Generated by Django 4.2 on 2023-04-30 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='progress',
            field=models.CharField(default=10, max_length=100),
            preserve_default=False,
        ),
    ]