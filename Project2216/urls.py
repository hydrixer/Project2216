"""
URL configuration for Project2216 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings

from iorder import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drinks', views.drink_list),
    path('drinks/<int:id>', views.drink_detail),
    path('pics/<int:pic_id>', views.pic),
    path('shop/<int:shop_id>', views.check_shop, name='check_shop'),
    path('shop', views.all_shop),
    path('addshop',views.add_shop),
    path('adddish',views.add_dish),
    path('menu/<int:shop_id>',views.get_menu),
    path('ownermenu',views.owner_menu),
    path('deletedish/<int:dish_id>',views.delete_dish),
    path('modifydish',views.modify_dish),
    path('register',views.register),
    path('login',views.login),
    path('orderhistory',views.order_history),
    path('alluser',views.all_user),
    path('changeuserinfo',views.change_userinfo),
    path('getinfobyusername',views.getinfobyusername),
    path('addorder',views.add_order)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)
