# Generated by Django 5.0.2 on 2024-02-21 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iorder', '0002_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='image',
            field=models.ImageField(default=None, upload_to='media/covers'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shop',
            name='image',
            field=models.ImageField(default=None, upload_to='media/covers'),
            preserve_default=False,
        ),
    ]
