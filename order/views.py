import jsonpickle as jsonpickle
from django.http import HttpResponseRedirect
from django.shortcuts import render
from cart.cartmanager import *

# Create your views here.
from django.views import View


class ToOrderView(View):
    def get(self, request):
        # 获取请求参数
        cartitems = request.GET.get('cartitems', '')

        # 判断用户是否登录
        if not request.session.get('user'):
            return render(request, 'login.html', {'cartitems': cartitems, 'redirect': 'order'})
        return HttpResponseRedirect('/order/order.html?cartitems='+cartitems)


class OrderList(View):
    def get(self, request):
        # 获取请求参数
        cartitems = request.GET.get('cartitems', '')
        # 将json格式字符串转换成python对象
        cartitemsList = jsonpickle.loads("["+cartitems+"]")

        # 将python对象转换成cartitems对象列表
        cartitemObjList = [getCartManger(request).get_cartitems(**item) for item in cartitemsList if item]

        # 1.获取用户默认收货地址
        address = request.session.get('user').address_set.get(isdefault=True)
        # 2.获取支付总金额
        totalPrice = 0
        for cm in cartitemObjList:
            totalPrice += cm.getTotalPrice()


        return render(request, 'order.html', {'cartitemList': cartitemObjList, 'address': address, 'totalPrice': totalPrice})