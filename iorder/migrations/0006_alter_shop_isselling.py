# Generated by Django 5.0.2 on 2024-02-27 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iorder', '0005_shop_dish_view_remove_shop_canteen_num_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='isselling',
            field=models.BooleanField(null=True),
        ),
    ]
