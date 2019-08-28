import jsonpickle as jsonpickle
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from cart.cartmanager import *
from utils.alipay import *

# Create your views here.
from django.views import View

from order.models import Order, OrderItem


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

# 创建alipay对象
alipay = AliPay(appid='2016092900622758', app_notify_url='http://127.0.0.1:8000/order/checkPay/', app_private_key_path='order/keys/my_private_key.txt',
                 alipay_public_key_path='order/keys/my_public_key.txt', return_url='http://127.0.0.1:8000/order/checkPay/', debug=True)
class ToPayView(View):
    def get(self, requset):
        # 获取请求参数
        import uuid,datetime
        data = {
            'out_trade_num': uuid.uuid4().hex,
            'order_num': datetime.datetime.today().strftime('%Y%m%d%H%M%S'),
            'pyway': requset.GET.get('payway'),
            'address': Address.objects.get(id=requset.GET.get('address', '')),
            'user': requset.session.get('user', '')
        }

        # 1.插入order表数据
        orderObj = Order.objects.create(**data)
        # 2.插入item表数据
        cartItems = jsonpickle.loads(requset.GET.get('cartitems'))

        orderItemList = [OrderItem.objects.create(order=orderObj, **item) for item in cartItems if item]

        totalPriceId = requset.GET.get('totalPriceId')[1:]

        # 获取扫码支付页面
        params = alipay.direct_pay(subject='京东超市', out_trade_no=orderObj.out_trade_num, total_amount=str(totalPriceId))

        # 拼接请求地址
        url = alipay.gateway+'?'+params
        return HttpResponseRedirect(url)


class CheckPayView(View):
    def get(self, request):
        # 校验是否支付成功（延签的过程）
        params = request.GET.dict()
        # 获取签名
        sign = params.pop('sign')

        if alipay.verify(params, sign):
            # 更改订单表中的状态
            out_trade_no = params.get('out_trade_no', '')
            order = Order.objects.get(out_trade_no=out_trade_no)
            order.status = '待发货'
            order.save()
            # 修改库存
            orderItemList = order.orderitem_set.all()
            [Inventory.objects.filter(goods_id=item.goodsid, size_id=item.sizeid, color_id=item.colorid).update(count=F('count')-item.count) for item in orderItemList if item]

            # 修改购物车
            [CartItem.objects.filter(goods_id=item.goodsid, size_id=item.sizeid, color_id=item.colorid).delete() for item in orderItemList if item]

            return HttpResponse('支付成功')
        return HttpResponse('支付失败')