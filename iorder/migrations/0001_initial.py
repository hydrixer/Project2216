# Generated by Django 5.0.2 on 2024-02-21 16:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dorm',
            fields=[
                ('dorm_index', models.IntegerField(primary_key=True, serialize=False)),
                ('building_num', models.SmallIntegerField()),
                ('room_num', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'dorm',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='drink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('shop_index', models.IntegerField(primary_key=True, serialize=False)),
                ('shop_name', models.TextField()),
                ('canteen_num', models.SmallIntegerField(blank=True, null=True)),
                ('floor', models.SmallIntegerField(blank=True, null=True)),
                ('isselling', models.IntegerField()),
            ],
            options={
                'db_table': 'shop',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(db_column='ID', max_length=15, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=10)),
                ('stu_num', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('emp_num', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('category', models.IntegerField()),
                ('admin_num', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'user',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('dish_index', models.IntegerField(primary_key=True, serialize=False)),
                ('dish_name', models.TextField()),
                ('price', models.IntegerField()),
                ('shop_index', models.ForeignKey(db_column='shop_index', on_delete=django.db.models.deletion.DO_NOTHING, to='iorder.shop')),
            ],
            options={
                'db_table': 'dish',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Stu',
            fields=[
                ('stu_num', models.DecimalField(decimal_places=0, max_digits=10, primary_key=True, serialize=False)),
                ('stu_name', models.TextField()),
                ('phonenumber', models.DecimalField(blank=True, decimal_places=0, max_digits=18, null=True)),
                ('dorm_index', models.ForeignKey(db_column='dorm_index', on_delete=django.db.models.deletion.DO_NOTHING, to='iorder.dorm')),
                ('id', models.ForeignKey(blank=True, db_column='ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='iorder.user')),
            ],
            options={
                'db_table': 'stu',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='OrderBill',
            fields=[
                ('order_num', models.BigIntegerField(primary_key=True, serialize=False)),
                ('dish_count', models.IntegerField()),
                ('price', models.IntegerField()),
                ('create_time', models.TimeField()),
                ('finished', models.IntegerField()),
                ('shop_index', models.IntegerField()),
                ('dish_index', models.ForeignKey(db_column='dish_index', on_delete=django.db.models.deletion.DO_NOTHING, to='iorder.dish')),
                ('stu_num', models.ForeignKey(blank=True, db_column='stu_num', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='iorder.stu')),
            ],
            options={
                'db_table': 'order_bill',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Emp',
            fields=[
                ('emp_num', models.DecimalField(decimal_places=0, max_digits=10, primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('shop_index', models.ForeignKey(db_column='shop_index', on_delete=django.db.models.deletion.DO_NOTHING, to='iorder.shop')),
                ('id', models.ForeignKey(blank=True, db_column='ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='iorder.user')),
            ],
            options={
                'db_table': 'emp',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_num', models.DecimalField(decimal_places=0, max_digits=10, primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('id', models.ForeignKey(blank=True, db_column='ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='iorder.user')),
            ],
            options={
                'db_table': 'admin',
                'managed': True,
            },
        ),
    ]
