from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from cart.cartmanager import *

# Create your views here.
from django.views import View
from .models import *

class RegisterView(View):
    def get(self, request):

        return render(request, 'register.html')

    def post(self, request):
        # 获取页面注册信息
        uname = request.POST.get('uname', '')
        pwd = request.POST.get('pwd', '')
        # 添加到数据库
        user = UserInfo.objects.create(uname=uname, pwd=pwd)
        if user:
            # 将用户信息存入到session中
            request.session['user'] = user
            return HttpResponseRedirect('/user/center/')

        return HttpResponseRedirect('/user/register/')


class CheckUnameView(View):
    def get(self, request):
        uname = request.GET.get('uname', '')
        # 数据库查询是否有新注册的
        unameList = UserInfo.objects.filter(uname=uname)
        # 定义变量
        flag = False
        # 判断
        if unameList:
            flag = True

        return JsonResponse({'flag': flag})


class CenterView(View):
    def get(self, request):

        return render(request, 'center.html')


class LoginOut(View):
    def post(self, request):
        # 删除session中的用户登录信息
        if 'user' in request.session:
            del request.session['user']

        return JsonResponse({'delflag': True})

import json
class Login(View):
    def get(self, request):
        # 获取请求参数
        red = request.GET.get('redirect', '')

        return render(request, 'login.html', {'redirect': red})

    def post(self, request):
        uname = request.POST.get('uname', '')
        pwd = request.POST.get('pwd', '')
        # 查询数据库中是否存在用户
        userList = UserInfo.objects.filter(uname=uname, pwd=pwd)
        if userList:
            request.session['user'] = userList[0]

            red = request.POST.get('redirect', '')
            if red == 'cart':
                # 将session中的购物项移动到用户中心
                SessionCartManager(request.session).migrateSession2DB()
                # 重定向
                return HttpResponseRedirect('/cart/queryAll/')
            elif red == 'order':
                return HttpResponseRedirect('/order/order.html?cartitems='+request.POST.get('cartitems', ''))

            return HttpResponseRedirect('/user/center/')
        return HttpResponseRedirect('/user/login/')

from utils.code import *
class LoadCode(View):
    def get(self, request):
        img, str = gene_code()
        # 将生成的验证码存入到session中
        request.session['sessionCode'] = str
        return HttpResponse(img, content_type='image/png')


class CheckCode(View):
    def get(self, request):
        # 获取输入框中的验证码
        code = request.GET.get('code', '')
        # 获取生成的验证码
        sessionCode = request.session.get('sessionCode', None)
        # 比较输入框中的code是否与session中的code相等
        flag = code == sessionCode

        return JsonResponse({'checkFlag': flag})


class AddressView(View):
    def get(self, request):
        user = request.session.get('user', '')
        # 获取当前登录用户的所有地址
        addrList = user.address_set.all()
        return render(request, 'address.html', {'addrList': addrList})

    def post(self, request):
        # 获取请求参数
        aname = request.POST.get('aname', '')
        aphone = request.POST.get('aphone', '')
        addr = request.POST.get('addr', '')
        user = request.session.get('user', '')
        # 将数据插入数据库
        address = Address.objects.create(aname=aname, aphone=aphone, addr=addr, userinfo=user, isdefault=(lambda count: True if count == 0 else False)(user.address_set.all().count()))

        # 获取当前登录用户的所有地址
        addrList = user.address_set.all()
        return render(request, 'address.html', {'addrList': addrList})

from django.core.serializers import serialize
class LoadAreaView(View):
    def get(self, request):
        # 获取请求参数
        pid = request.GET.get('pid', -1)
        pid = int(pid)
        areaList = Area.objects.filter(parentid=pid)

        # 进行序列化
        jareaList = serialize('json', areaList)
        return JsonResponse({'jareaList': jareaList})
