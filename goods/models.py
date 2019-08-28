from django.db import models

# Create your models here.

# 商品类别
class Category(models.Model):
    cname = models.CharField(max_length=10)

    def __str__(self):
        return u'Category:%s' % self.cname
# 商品信息
class Goods(models.Model):
    gname = models.CharField(max_length=100)
    gdesc = models.CharField(max_length=100)
    oldprice = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return u'Goods:%s' % self.gname

    # 获取商品大图
    def getGImg(self):
        return self.inventory_set.first().color.colorurl

    # 获取商品颜色
    def getColor(self):
        colorList = []
        for inventory in self.inventory_set.all():
            color = inventory.color
            if color not in colorList:
                colorList.append(color)
        return colorList

    # 获取商品尺寸
    def getSize(self):
        sizeList = []
        for inventory in self.inventory_set.all():
            size = inventory.size
            if size not in sizeList:
                sizeList.append(size)
        return sizeList

    # 获取图片详情
    def getDetailList(self):
        import collections
        # 创建有序字典存放详情信息
        datas = collections.OrderedDict()

        for goodsDetail in self.goodsdetail_set.all():
            gdname = goodsDetail.name()
            if gdname not in datas:
                datas[gdname] = [goodsDetail.gdurl]
            else:
                datas[gdname].append(goodsDetail.gdurl)

        return datas


# 详细信息名称
class GoodsDetailname(models.Model):
    gdname = models.CharField(max_length=30)

    def __str__(self):
        return u'GoodsDetailname:%s' % self.gdname
# 详细信息
class GoodsDetail(models.Model):
    gdurl = models.ImageField(upload_to='')
    gdname = models.ForeignKey(GoodsDetailname, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)

    def name(self):
        return self.gdname.gdname


# 商品尺寸
class Size(models.Model):
    sname = models.CharField(max_length=10)

    def __str__(self):
        return u'Size:%' % self.sname

# 商品颜色
class Color(models.Model):
    colorname = models.CharField(max_length=10)
    colorurl = models.CharField(max_length=200)

    def __str__(self):
        return u'Color:%' % self.colorname

# 关联商品信息
class Inventory(models.Model):
    count = models.PositiveIntegerField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)