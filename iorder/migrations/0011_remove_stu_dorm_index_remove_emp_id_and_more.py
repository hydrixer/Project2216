# Generated by Django 5.0.2 on 2024-02-27 23:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iorder', '0010_rename_id_user_username_user_email_user_telephone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stu',
            name='dorm_index',
        ),
        migrations.RemoveField(
            model_name='emp',
            name='id',
        ),
        migrations.RemoveField(
            model_name='emp',
            name='shop_index',
        ),
        migrations.RemoveField(
            model_name='stu',
            name='id',
        ),
        migrations.RemoveField(
            model_name='orderbill',
            name='stu_num',
        ),
        migrations.AddField(
            model_name='orderbill',
            name='client',
            field=models.ForeignKey(blank=True, db_column='ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='iorder.user'),
        ),
        migrations.AddField(
            model_name='shop',
            name='host',
            field=models.ForeignKey(blank=True, db_column='ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='iorder.user'),
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
        migrations.DeleteModel(
            name='Dorm',
        ),
        migrations.DeleteModel(
            name='Emp',
        ),
        migrations.DeleteModel(
            name='Stu',
        ),
    ]