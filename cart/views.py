from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import View
from .cartmanager import *


class AddCartView(View):
    def post(self, request):
        # 在多级字典数据的时候，需要手动设置modified=True，实时将数据存入到session中
        request.session.modified = True

        # 1.获取当前操作类型
        flag = request.POST.get('flag', '')
        # 创建CartManager对象
        cartManagerObj = getCartManger(request)
        # 2.判断当前操作类型
        if flag == 'add':
            # 加入购物车操作
            cartManagerObj.add(**request.POST.dict())
        elif flag == 'plus':
            # 添加数量
            cartManagerObj.update(step=1, **request.POST.dict())
        elif flag == 'minus':
            # 减少数量
            cartManagerObj.update(step=-1, **request.POST.dict())
        elif flag == 'delete':
            # 逻辑删除
            cartManagerObj.delete(**request.POST.dict())
        return HttpResponseRedirect('/cart/queryAll/')


class QueryAllView(View):
    def get(self, request):
        # 创建CartManager对象
        cartManagerObj = getCartManger(request)
        # 查询所有购物项信息
        cartList = cartManagerObj.queryAll()

        return render(request, 'cart.html', {'cartList': cartList})



