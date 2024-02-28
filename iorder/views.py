import os

from django.core.serializers import serialize
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from iorder.models import drink, Pic, Shop, User, OrderBill, Dish
from iorder.serializers import Drinkserializer
from iorder.sqlview import shop_dish_view


@api_view(['GET','POST'])
def drink_list(request, format=None):
    if request.method=='GET':
        drinks = drink.objects.all()
        serializer = Drinkserializer(drinks,many=True)
        return Response(serializer.data)
    else:
        serializer = Drinkserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def drink_detail(request,id, format=None):
    try:
        drk=drink.objects.get(pk=id)
    except drk.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET':
        serializer = Drinkserializer(drk)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer =Drinkserializer(drk,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data)
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        drk.delete()

def pic(request, pic_id):
    pic = Pic.objects.get(pk = pic_id)
    if pic is not None:
        return render(request, 'pics/pics.html', {'pics': pic})
    else:
        raise Http404('no such image!')


def check_shop(request, shop_id):
    try:
        shop = Shop.objects.get(pk=shop_id)
        shop_dish = shop_dish_view.objects.all()

        shop_data = {
            "code": 200,
            "msg": "success",
            "data":{
                    'shop_index': shop.shop_index,
                    'name': shop.shop_name,
                    'isselling': shop.isselling,
                    'logo': shop.image.url if shop.image else None
            }
        }
        return JsonResponse(shop_data, safe=False)
    except Shop.DoesNotExist:
        return JsonResponse({'error': 'Shop not found'}, status=404)

def all_shop(request):
    try:
        first_shops = Shop.objects.all()
        list=[]
        for ashop in first_shops:
            list.append(
                {
                    'shop_index': ashop.shop_index,
                    'name': ashop.shop_name,
                    'isselling': ashop.isselling,
                    'logo': ashop.image.url if ashop.image else None,
                }
            )
        shop_data = {
            "code": 200,
            "msg": "success",
            "data":{
                "list": list
            }
        }
        return JsonResponse(shop_data, safe=False)
    except Shop.DoesNotExist:
        return JsonResponse({'error': 'Shop not found'}, status=404)


@csrf_exempt
@api_view(['POST'])
def add_shop(request, format=None):
        data = request.data
        try:
            new_shop = Shop.objects.create(
                shop_name=data.get('shop_name'),
                shop_index=Shop.objects.count(),
                isselling=True,
                host=User.objects.get(data.get('username'))
            )
            image_file = request.FILES.get('image')
            if image_file:
                new_shop.image = image_file
            new_shop.save()

            return JsonResponse({'message': 'Shop created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def check_dish(request, dish_index, shop_index,format=None):
    try:
        dish = Dish.objects.get(dish_index=dish_index, shop_index=shop_index)
        dish_data = {
            "code": 200,
            "msg": "success",
            "data": {
                'dish_index': dish.dish_index,
                'dish_name': dish.dish_name,
                'price': dish.price,
                'vegan': dish.vegan,
                'image': dish.image.url if dish.image else None,
            }
        }
        return JsonResponse(dish_data, safe=False)
    except Dish.DoesNotExist:
        return JsonResponse({'error': 'Dish not found'}, status=404)

def get_dish_list(queryset):
    dish_list = []
    for dish in queryset:
        dish_list.append({
            'dish_index': dish.dish_index,
            'dish_name': dish.dish_name,
            'price': dish.price,
            'vegan': dish.vegan,
            'image': dish.image.url if dish.image else None,
        })
    return dish_list

def all_dish(request,shop_index):
    try:
        first_dish = Dish.objects.filter(shop_index=shop_index)
        dish_list = get_dish_list(first_dish)
        dish_data = {
            "code": 200,
            "msg": "success",
            "data":{
                "list": dish_list
            }
        }
        return JsonResponse(dish_data, safe=False)
    except Shop.DoesNotExist:
        return JsonResponse({'error': 'Dish not found'}, status=404)

# def all_vegan_dish(request,shop_index):
#     try:
#         first_vegan_dish = Dish.objects.filter(vegan=True,shop_index=shop_index)
#         dish_list = get_dish_list(first_vegan_dish)
#         dish_data = {
#             "code": 200,
#             "msg": "success",
#             "data":{
#                 "list": dish_list
#             }
#         }
#         return JsonResponse(dish_data, safe=False)
#     except Shop.DoesNotExist:
#         return JsonResponse({'error': 'Vegan dish not found'}, status=404)

@api_view(['POST'])
def add_dish(request, format=None):
        data = request.data
        try:
            new_dish = Dish.objects.create(
                dish_index=Dish.objects.count(),
                dish_name=data.get('dish_name'),
                shop_index=Shop.objects.get(shop_index=data.get('shop_index')),
                price=data.get('price'),
                description=data.get('description'),
                vegan = True if data.get('vegan') == "true" else False,
            )
            image_file = request.FILES.get('image')
            if image_file:
                new_dish.image = image_file
            new_dish.save()

            return JsonResponse({'message': 'Dish created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@api_view(['DELETE'])
def delete_dish(request, dish_id):
    try:
        dish = Dish.objects.get(dish_index=dish_id)
        image_path = dish.image
        if os.path.exists(image_path):
            # 删除文件
            os.remove(image_path)
        else:
            print(f"The file {image_path} does not exist.")
        dish.delete()
        return  JsonResponse({'message': 'Dish deleted successfully'}, status=201)
    except Exception as e:
        return  JsonResponse({'error:': str(e)}, status=400)

@api_view(['GET'])
def get_menu(request, shop_id):
    try:
        mymenu = Dish.objects.filter(shop_index=shop_id)
        list=[]
        for dish in mymenu:
            list.append(
                {
                    'dish_index': dish.dish_index,
                    'shop_index': dish.shop_index.shop_index,
                    'dish_name': dish.dish_name,
                    'price':dish.price,
                    'vegan': dish.vegan,
                    'description':dish.description,
                    'image': dish.image.url if dish.image else None,
                }
            )
        menu_data = {
            "code": 200,
            "msg": "success",
            "data":{
                "list": list
            }
        }
        return JsonResponse(menu_data, safe=False)
    except Dish.DoesNotExist:
        return JsonResponse({'error': 'Shopmenu not found'}, status=404)


def user_detail(request, user_id, format=None):
    try:
        user = User.objects.get(id=user_id)
        user_data = {
            "code": 200,
            "msg": "success",
            "data": {
                'id': user.id,
                'password':user.password,
                'stu_num': user.stu_num,
                'emp_num': user.emp_num,
                'category': user.category,
                'admin_num': user.admin_num,
            }
        }
        return JsonResponse(user_data, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@api_view(['POST','GET'])
def order_history(request, format=None):
    try:
        user = User.objects.get(username=request.data.get('username'))
        category = user.category
        if(category==1): #user
            userhistory = OrderBill.objects.filter(client=user)
            list = []
            for aorder in userhistory:
                list.append(
                    {
                        'dish_name': aorder.dish_index.dish_name,
                        'dish_count': aorder.dish_count,
                        'tablenumber': aorder.table,
                        'create_time': aorder.create_time,
                        'note': aorder.note,
                        'finished': aorder.finished,
                    }
                )
            order_data = {
                "code": 200,
                "msg": "success",
                "data": {
                    "list": list
                }
            }
        elif(category==2):
            userhistory = OrderBill.objects.filter(user.shop)
            list = []
            for aorder in userhistory:
                list.append(
                    {
                        'dish_name': aorder.dish_index.dish_name,
                        'dish_count': aorder.dish_count,
                        'tablenumber': aorder.table,
                        'create_time': aorder.create_time,
                        'note': aorder.note,
                        'finished': aorder.finished,
                    }
                )
            order_data = {
                "code": 200,
                "msg": "success",
                "data": {
                    "list": list
                }
            }
        return JsonResponse(order_data, safe=False)
    except OrderBill.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)



# @api_view(['POST'])
# def place_order(request):
#


@api_view(['POST'])
def register(request):
    data = request.data
    user1 = User.objects.filter(username=data.get('username')).first()
    if user1 is not None:
        return JsonResponse({'error': 'username occupied'}, status=400)
    try:
        new_user = User.objects.create(
            username=data.get('username'),
            password=data.get('password'),
            category = data.get('category'),
            telephone = data.get('telephone'),
            email = data.get('email')
        )
        new_user.save()
        return JsonResponse({'message': 'Account created successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@api_view(['GET'])
def login(request):
    data = request.data
    user1= User.objects.get(data.get('username'))
    if user1 is not None:
        return JsonResponse({'error: user not found'}, status=400)
    elif user1.password==data.get('password'):
        login_data = {
            "code": 200,
            "msg": "success",
            "data": {
                'result':1
            }
        }
    else:
        login_data = {
            "code": 888,
            "msg": "Failed",
            "data": {
                'result': 0
            }
        }
    return JsonResponse(login_data, safe=False)

# Create your views here.
