# Generated by Django 3.2.5 on 2023-02-18 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]