from rest_framework import generics, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import MenuItem, Cart, Order
from .serializers import MenuItemSerializer, UserSerializer, CartSerializer, OrderSerializer
from django.contrib.auth.models import User,Group
from django.core.paginator import Paginator, EmptyPage
@api_view(['GET','POST','DELETE','PUT','PATCH'])
@permission_classes([IsAuthenticated])
def menu_item_list(request):
    if request.method == 'GET':
        menu_items = MenuItem.objects.all()
        #check for pagination
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        ordering = request.query_params.get('ordering', default='id')
        if ordering:
            orderingfeilds = ordering.split(',')
            menu_items = MenuItem.objects.all().order_by(*orderingfeilds)
        paginator = Paginator(menu_items, perpage)
        try:
            menu_items = paginator.page(page)
        except EmptyPage:
            menu_items = paginator.page(paginator.num_pages)
        serializer = MenuItemSerializer(menu_items, many=True)


        return Response(serializer.data)
    else:

        user = request.user
        #check if user group
        if not user.groups.filter(name='Manager').exists():
            if request.method == "POST":
                serializer = MenuItemSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': '404 – Not Found'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'message': '403 – Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)



@api_view(['GET','POST','DELETE','PUT','PATCH'])
@permission_classes([IsAuthenticated])
def menu_single_item_list(request,menuItem):
    if request.method == 'GET':
        menu_items = MenuItem.objects.all().filter(title=menuItem)
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data)
    else:

        user = request.user
        #check if user group
        if not user.groups.filter(name='Manager').exists():
            if request.method == "POST":
                return Response({'message': '404 – Not Found'}, status=status.HTTP_404_NOT_FOUND)
            elif request.method == "PUT" or request.method == "PATCH":
                menu_items = MenuItem.objects.all().filter(title=menuItem)
                if menu_items:
                    menu_items = menu_items[0]
                    serializer = MenuItemSerializer(menu_items, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': '404 – Not Found'}, status=status.HTTP_404_NOT_FOUND)
            elif request.method == "DELETE":
                menu_items = MenuItem.objects.all().filter(title=menuItem)
                if menu_items:
                    menu_items = menu_items[0]
                    menu_items.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({'message': '404 – Not Found'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'message': '403 – Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)



@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def manager_users(request):
    user = request.user
    if user.groups.filter(name='Manager').exists():
        if request.method == "GET":
            users = User.objects.all().filter(groups__name='Manager')
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                group = Group.objects.get(name='Manager')
                user.groups.add(group)
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': '403 – Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def manager_users_single(request,userId):
    user = request.user
    if user.groups.filter(name='Manager').exists():
        if request.method == "DELETE":
            users = User.objects.all().filter(groups__name='Manager',id=userId)
            if users:
                users = users[0]
                users.delete()
                return Response(status=status.HTTP_200_OK)

            else:
                return Response({'message': '404 – Not Found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message': '403 – Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def delivery_crew_users(request):
    user = request.user
    if user.groups.filter(name='Manager').exists():
        if request.method == "GET":
            users = User.objects.all().filter(groups__name='delivery crew')
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                group = Group.objects.get(name='delivery crew')
                user.groups.add(group)
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delivery_crew_users_single(request,userId):
    user = request.user
    if user.groups.filter(name='Manager').exists():
        if request.method == "DELETE":
            users = User.objects.all().filter(groups__name='delivery crew',id=userId)
            if users:
                users = users[0]
                users.delete()
                return Response(status=status.HTTP_200_OK)

            else:
                return Response({'message': '404 – Not Found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message': '403 – Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def cart_menu_item(request):
    user = request.user
    if user.groups.filter(name='Customer').exists():
        if request.method == "GET":
            cart = Cart.objects.all().filter(user=user)
            serializer = CartSerializer(cart, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = CartSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            #delete all cart items by user
            cart = Cart.objects.all().filter(user=user)
            cart.delete()
            return Response(status=status.HTTP_200_OK)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def orders(request):
    user = request.user
    if user.groups.filter(name='Customer').exists():
        if request.method == "GET":
            orders = Order.objects.all().filter(user=user)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif user.groups.filter(name='Manager').exists():
        if request.method == "GET":
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)
    elif user.groups.filter(name='delivery crew').exists():
        if request.method == "GET":
            orders = Order.objects.all().filter(delivery_crew=user)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)


@api_view(['GET', 'POST','PUT','PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def single_order(request,orderId):
    user = request.user
    if user.groups.filter(name='Customer').exists():
        if request.method == "GET":
            orders = Order.objects.all().filter(user=user,id=orderId)
            if orders:
                serializer = OrderSerializer(orders, many=True)
                return Response(serializer.data)
            else:
                return Response({'message': '404 – Not Found'}, status=status.HTTP_404_NOT_FOUND)
        elif request.method == "PUT" or request.method == "PATCH":
            orders = Order.objects.all().filter(user=user,id=orderId)
            if orders:
                serializer = OrderSerializer(orders[0], data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': '404 – Not Found'}, status=status.HTTP_404_NOT_FOUND)
        elif request.method == "DELETE":
            return Response({'message': '403 – Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)
    elif user.groups.filter(name='Manager').exists():
        if request.method == "GET":
            orders = Order.objects.all().filter(id=orderId)
            if orders:
                serializer = OrderSerializer(orders, many=True)
                return Response(serializer.data)
            else:
                return Response({'message': '404 – Not Found'}, status=status.HTTP_404_NOT_FOUND)
        elif request.method == "PUT" or request.method == "PATCH":
            orders = Order.objects.all().filter(id=orderId)
            if orders:
                serializer = OrderSerializer(orders[0], data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': '404 – Not Found'}, status=status.HTTP_404_NOT_FOUND)
        elif request.method == "DELETE":
            orders = Order.objects.all().filter(id=orderId)
            if orders:
                orders[0].delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': '404 – Not Found'}, status=status.HTTP_404_NOT_FOUND)
    elif user.groups.filter(name='delivery crew').exists():
        if request.method == "GET":
            orders = Order.objects.all().filter(delivery_crew=user,id=orderId)
            if orders:
                serializer = OrderSerializer(orders, many=True)
                return Response(serializer.data)
            else:
                return Response({'message': '404 – Not Found'}, status=status.HTTP_404_NOT_FOUND)
        elif request.method == "PUT" or request.method == "PATCH":
            orders = Order.objects.all().filter(delivery_crew=user,id=orderId)
            if orders:
                serializer = OrderSerializer(orders[0], data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': '404 – Not Found'}, status=status.HTTP_404_NOT_FOUND)
        elif request.method == "DELETE":
            return Response({'message': '403 – Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)


