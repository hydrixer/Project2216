# Generated by Django 5.0.2 on 2024-02-22 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iorder', '0003_dish_image_shop_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='vegan',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
