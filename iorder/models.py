from django.db import models

class drink(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name +' FREE!'



class Admin(models.Model):
    admin_num = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    id = models.ForeignKey('User', models.DO_NOTHING, db_column='ID', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'admin'


class Dish(models.Model):
    dish_index = models.IntegerField(primary_key=True)
    dish_name = models.TextField()
    shop_index = models.ForeignKey('Shop', models.DO_NOTHING, db_column='shop_index')
    price = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'dish'


class Dorm(models.Model):
    dorm_index = models.IntegerField(primary_key=True)
    building_num = models.SmallIntegerField()
    room_num = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'dorm'


class Emp(models.Model):
    emp_num = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    id = models.ForeignKey('User', models.DO_NOTHING, db_column='ID', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(blank=True, null=True)
    shop_index = models.ForeignKey('Shop', models.DO_NOTHING, db_column='shop_index')

    class Meta:
        managed = True
        db_table = 'emp'


class OrderBill(models.Model):
    order_num = models.BigIntegerField(primary_key=True)
    dish_index = models.ForeignKey(Dish, models.DO_NOTHING, db_column='dish_index')
    stu_num = models.ForeignKey('Stu', models.DO_NOTHING, db_column='stu_num', blank=True, null=True)
    dish_count = models.IntegerField()
    price = models.IntegerField()
    create_time = models.TimeField()
    finished = models.IntegerField()
    shop_index = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'order_bill'


class Shop(models.Model):
    shop_index = models.IntegerField(primary_key=True)
    shop_name = models.TextField()
    canteen_num = models.SmallIntegerField(blank=True, null=True)
    floor = models.SmallIntegerField(blank=True, null=True)
    isselling = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'shop'


class Stu(models.Model):
    stu_num = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    id = models.ForeignKey('User', models.DO_NOTHING, db_column='ID', blank=True, null=True)  # Field name made lowercase.
    stu_name = models.TextField()
    dorm_index = models.ForeignKey(Dorm, models.DO_NOTHING, db_column='dorm_index')
    phonenumber = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stu'


class User(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=15)  # Field name made lowercase.
    password = models.CharField(max_length=10)
    stu_num = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    emp_num = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    category = models.IntegerField()
    admin_num = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user'

