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



@api_view(['POST','GET'])
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
                    'image': ashop.image.url if ashop.image else None,
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

def check_shop(request, shop_id):
    try:
        shop = Shop.objects.get(pk=shop_id)

        shop_data = {
            "code": 200,
            "msg": "success",
            "data":{
                    'shop_index': shop.shop_index,
                    'name': shop.shop_name,
                    'isselling': shop.isselling,
                    'image': shop.image.url if shop.image else None
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
                host=User.objects.get(username=data.get('username'))
            )
            image_file = request.FILES.get('image')
            if image_file:
                new_shop.image = image_file
            new_shop.save()

            return JsonResponse({'message': 'Shop created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)



@api_view(['GET','POST'])
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
            username=data.get('username')
            user = User.objects.get(username=username)
            new_dish = Dish.objects.create(
                dish_index=Dish.objects.count(),
                dish_name=data.get('dish_name'),
                shop_index=user.shop,
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


@api_view(['POST'])
def modify_dish(request, format=None):
        data = request.data
        try:
            modify_dish = Dish.objects.get(dish_index=data.get('dish_index'))
            default_vegan = modify_dish.vegan
            modify_dish.dish_name = data.get('dish_name')
            modify_dish.price = data.get('price')
            modify_dish.description = data.get('description')
            modify_dish.vegan = True if data.get('vegan',default_vegan) == True else False
            image_file = request.FILES.get('image')
            if image_file:
                modify_dish.image = image_file
            modify_dish.save()

            return JsonResponse({'message': 'Dish modified successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@api_view(['DELETE'])
def delete_dish(request, dish_id):
    try:
        dish = Dish.objects.get(dish_index=dish_id)
        if dish.image is not None:
            dish.image.delete()
        else:
            print(f"The file  does not exist.")
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


@api_view(['GET','POST'])
def owner_menu(request):
    if request.method == 'POST':
        username = request.data.get('username')
        # 对于GET请求，从URL参数中获取username
    else:
        username = request.query_params.get('username')
    try:
        shop = Shop.objects.get(host=User.objects.get(username=username))
        shop_dish = Dish.objects.filter(shop_index=shop.shop_index)
        list = []
        for dish in shop_dish:
            list.append(
                {
                    'dish_index': dish.dish_index,
                    'shop_index': dish.shop_index.shop_index,
                    'dish_name': dish.dish_name,
                    'price': dish.price,
                    'vegan': dish.vegan,
                    'description': dish.description,
                    'image': dish.image.url if dish.image else None,
                }
            )
        shop_data = {
            "code": 200,
            "msg": "success",
            "data":{
                "list":list
            }
        }
        return JsonResponse(shop_data, safe=False)
    except Shop.DoesNotExist:
        return JsonResponse({'error': 'Shop not found'}, status=404)



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

@api_view(['GET'])
def order_history(request, format=None):
    try:
        user = User.objects.get(username=request.query_params.get('username'))
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
            userhistory = OrderBill.objects.filter(shop_index=user.shop.shop_index)
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


@api_view(['POST'])
def login(request):
    data = request.data
    user1 = User.objects.filter(username=data.get('username')).first()
    if user1 is None:
        return JsonResponse({'error: user not found'}, status=400)
    elif user1.password==data.get('password'):
        login_data = {
            "code": 200,
            "msg": "success",
            "data": {
                'result':1,
                'username':user1.username,
                'password':user1.password,
                'telephone':user1.telephone,
                'email':user1.email,
                'category':user1.category,
                'token':user1.token
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


@api_view(['POST'])
def change_userinfo(request):
    try:
        data = request.data
        usertochange = User.objects.get(username=data.get('username'))
        telephone = data.get('telephone')
        if telephone is not None and telephone != '':
            usertochange.telephone = telephone
        email = data.get('email')
        if email is not None and telephone != '':
            usertochange.email=email
        usertochange.save()
        return JsonResponse({'message': 'info changed successfully'}, status=201)
    except User.DoesNotExist:
        return JsonResponse({'error': 'user not found'}, status=404)

@api_view(['GET'])
def all_user(request):
    try:
        allusers = User.objects.all()
        list=[]
        for user in allusers:
            list.append(
                {
                    'username':user.username,
                    'password':user.password
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
    except Exception as e:
        return JsonResponse({'error:': str(e)}, status=400)


@api_view(['GET'])
def getinfobyusername(request):
    try:
        username = request.query_params.get('username')
        user = User.objects.get(username=username)
        info_data = {
            "code": 200,
            "msg": "success",
            "data": {
                'username':user.username,
                'password':user.password,
                'telephone':user.telephone,
                'category':user.category,
                'email':user.email,
                'token':user.token
            }
        }
        return JsonResponse(info_data, safe=False)
    except Exception as e:
        return JsonResponse({'error:': str(e)}, status=400)


@api_view(['POST'])
def add_order(request):
    try:
        data = request.data
        for order_data in data:
            new_order= OrderBill.objects.create(
                order_num=OrderBill.objects.count(),
                price=int(order_data.get('price'))*int(order_data.get('quantity')),
                dish_count=order_data.get('quantity'),
                finished=order_data.get('state'),
                table=order_data.data.get('tableNum'),
                note=order_data.get('note'),
                dish_index=Dish.objects.get(dish_index=order_data.get('dish_index')),
                client= User.objects.get(username=order_data.get('username'))
            )
            new_order.save()
        return JsonResponse({'message': 'info changed successfully'}, safe=False)
    except Exception as e:
        return  JsonResponse({'error': str(e)}, status=400)
# Create your views here.
