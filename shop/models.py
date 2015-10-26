# -*- coding: UTF-8 -*-
__author__ = 'Konstantyn Davidenko'
from django.db import models
from stdimage import StdImageField
# from stdimage.utils import UploadToUUID, UploadToClassNameDir, UploadToAutoSlug, UploadToAutoSlugClassNameDir
from transliterate import translit

# print translit(u"Кольцо", reversed=True)

def file_path(self, filename):
    return translit(u"{cat}/img/{filename}".format(cat=self.category, filename=filename), reversed=True)


class Contacts(models.Model):
    phone = models.TextField(verbose_name='номер телефона')
    skype = models.CharField(verbose_name='скайп аккаунт', max_length=20)
    mail = models.CharField(verbose_name='почта', max_length=20)


class Brand(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название брэнда', unique=True)
    # image = StdImageField(verbose_name="Картинка Брэнда", upload_to='static/upload/brands',
    #                       variations={'thumbnail': {'with': 165, 'height': 160}})

    def __unicode__(self):
        return self.name

    def get_url(self):
        url = '/%s/%s' % (self.part.id, self.id)
        print url
        return url


class Material(models.Model):
    name = models.CharField(verbose_name="Материал", blank=True, unique=True, default="Серебро 925 ALE", max_length=30)

    def __unicode__(self):
        return self.name


class Incrustation(models.Model):
    name = models.CharField(verbose_name="Инкрустация", max_length=30, blank=True, unique=True)

    def __unicode__(self):
        return self.name


class LowerCaseCharField(models.CharField):
    """
    Defines a charfield which automatically converts all inputs to
    lowercas
    """

    def __init__(self, *args, **kwargs):
        models.CharField.__init__(self, *args, **kwargs)

    def to_python(self, value):
        value = super(LowerCaseCharField, self).to_python(value)
        if isinstance(value, basestring):
            return value.lower()
        return value


class Part(models.Model):
    name = models.CharField(verbose_name='Раздел', max_length=100)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(verbose_name="Категория", blank=False, max_length=50, unique=True)
    part = models.ForeignKey(Part, verbose_name='Раздел')

    def __unicode__(self):
        return self.name

    def get_url(self):
        url = '/%s/%s' % (self.part.id, self.id)
        print url
        return url


class Size(models.Model):
    size = models.FloatField(verbose_name='Размер')

    def __unicode__(self):
        return str(self.size)

class Available(models.Model):
    name = models.CharField(verbose_name="Наличие", max_length=20)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    GENDER_CHOICES = (
        ('M', 'Мужское'),
        ('F', 'Женское'),
    )
    part = models.ForeignKey(Part, verbose_name="Раздел")
    category = models.ForeignKey(Category, verbose_name="Под Раздел")
    name = models.CharField(verbose_name='Название', max_length=50)
    description = models.CharField(verbose_name='Описание', max_length=1000, default=' ')
    price = models.IntegerField(verbose_name='Цена')
    rating = models.IntegerField(verbose_name="Рейтинг", default=1)
    incrustation = models.ForeignKey(Incrustation, verbose_name="Инкрустация")
    brand = models.ForeignKey(Brand, verbose_name="Брэнд")
    material = models.ForeignKey(Material, verbose_name="Материал")
    date_add = models.DateField(verbose_name="Дата добавления товара", blank=False, auto_now=True)
    image = StdImageField(upload_to=file_path, variations={'thumbnail': {'with': 165, 'height': 160}})
    size = models.ForeignKey(Size, verbose_name='Размер')
    gender = models.CharField(max_length=1, verbose_name="Для кого", choices=GENDER_CHOICES)
    availability = models.ForeignKey(Available, verbose_name="Наличие")

    def __unicode__(self):
        return self.name


class Comment(models.Model):
    comment = models.TextField(verbose_name='Коментарий', max_length=1000)
    product = models.ForeignKey(Product, related_name='comment', verbose_name='Коментарий для товара')
    date_add = models.DateTimeField(verbose_name="Дата добавления коментария", blank=False, auto_now=True)
    author = models.CharField(verbose_name='Автор', max_length=100)

    def __unicode__(self):
        return self.comment

class Order(models.Model):
    pass

class ConfirmedOrder(models.Model):
    pass

class Compare(models.Model):
    session_id = models.CharField(verbose_name='Номер Сессии', max_length=64)
    product = models.ForeignKey(Product, verbose_name='Товар')

    def __unicode__(self):
        return str(self.session_id)