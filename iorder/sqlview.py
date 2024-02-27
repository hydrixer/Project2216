from django.db import models

class shop_dish_view(models.Model):
    shop_name = models.TextField()
    dish_name = models.TextField()
    price = models.IntegerField()
    vegan = models.BooleanField()

    class Meta:
        managed = False  # 设置为False以告诉Django这是一个不受Django管理的视图
        db_table = 'shop_dishes_view'  # 设置为视图的名称