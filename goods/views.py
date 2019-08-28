import math
from django.shortcuts import render

# Create your views here.
from django.views import View
from .models import *
from django.core import paginator


class IndexView(View):
    def get(self, request, cid=1, num=1):
        cid = int(cid)
        num = int(num)
        # 查询当前类
        category = Category.objects.all().order_by('id')

        # 查询当前类别下的商品
        goodsList = Goods.objects.filter(category_id=cid).order_by('id')

        # 分页查询（每页8条记录）
        pager = paginator.Paginator(object_list=goodsList, per_page=8)
        goods_pageList = pager.page(num)

        # 页码数越界限制
        begin = (num - int(math.ceil(10.0/2)))
        if num < 1:
            begin = 1
        end = begin + 9
        if end > pager.num_pages:
            end = pager.num_pages

        if end <= 10:
            begin = 1
        else:
            begin = end - 9

        pageList = range(begin, end+1)

        return render(request, 'index.html', {'category': category, 'cur_Cateid': cid, 'goodsList': goods_pageList, 'pageList': pageList, 'cur_Page': num})


# 装饰器来装饰get方法，创建cookie返回到页面
# 先创建cookie，在获取进行查询
def recommend_view(func):
    def _wrapper(detailView, request, goodsid, *args, **kwargs):

        # 获取存放在cookie中的id
        cookie_list = request.COOKIES.get('recommend', '')

        # 存放所有goodsid的列表
        goodsIdList = [gid for gid in cookie_list.split() if gid.strip()]

        # 存放所有goods对象的列表
        goodsObjList = [Goods.objects.get(id=gsid) for gsid in goodsIdList if gsid != goodsid and Goods.objects.get(id=gsid).category_id == Goods.objects.get(id=goodsid).category_id][:4]

        # 将goodsObjList传给get方法
        response = func(detailView, request, goodsid, goodsObjList, *args, **kwargs)

        # 判断goodsid是否存在goodsList中
        if goodsid in goodsIdList:
            goodsIdList.remove(goodsid)
            goodsIdList.insert(0, goodsid)
        else:
            goodsIdList.insert(0, goodsid)

        # 将goodsIdList存放到cookie中，字符串的形式存入
        response.set_cookie('recommend', ' '.join(goodsIdList), max_age=3*24*60*60)

        return response
    return _wrapper

class GoodsDetailView(View):
    @recommend_view
    def get(self, request, goodsid, recommendList=[]):
        # 根据goodsID查询商品信息
        goods = Goods.objects.get(id=goodsid)

        return render(request, 'detail.html', {'goods': goods, 'recommendList': recommendList})