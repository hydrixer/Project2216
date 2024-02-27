from django.contrib import admin
from django.contrib import admin
from .models import *

class PicAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(drink)
admin.site.register(User)
admin.site.register(Dish)
admin.site.register(Emp)
admin.site.register(Pic,PicAdmin)
admin.site.register(Shop)
# Register your models here.
