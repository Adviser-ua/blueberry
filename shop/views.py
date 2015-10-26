# -*- coding: UTF-8 -*-
__author__ = 'Konstantyn Davidenko'


from django.views.generic import TemplateView
from models import Product, Category as Cat, Part, Comment, Brand, Incrustation, Size, Material, Compare
from django.shortcuts import render
from django.views.generic import View
from cart import Cart
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from forms import CommenForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

def get_comments(product_id):
    return Comment.objects.filter(product=product_id).order_by('date_add')


def session_setting(request):
    pass

def get_kwrgs(request):
    kwargs = {}
    kwargs['cart'] = Cart(request)
    kwargs['categories'] = Cat.objects.all()
    # kwargs['form'] = RegisterFormView()
    kwargs['parts'] = Part.objects.all()
    kwargs['session'] = request.session
    return kwargs


class Login(View):

    def get(self, request):
        return render(request, 'shop/login_form.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        print username, password
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                last_url = request.META['HTTP_REFERER']
                return HttpResponseRedirect(redirect_to=last_url)
        return HttpResponseRedirect(redirect_to='/')


class Register(View):

    def get(self, request):
        return render(request, 'base.html')

    def post(self, request):
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']


class Logout(View):

    def get(self, request):
        logout(request)
        last_url = request.META['HTTP_REFERER']
        return HttpResponseRedirect(redirect_to=last_url)


class UserAccount(View):
    template_name = 'shop/user_acc.html'

    def get(self, request):
        kwrgs = get_kwrgs(request)
        return render(request, self.template_name, kwrgs)


def append_product(query_sets):
    result = []
    for query_set in query_sets:
        for item in query_set:
            result.append(item)
    return result


def find(query=None):
    if query.isdigit():
        finded_id = Product.objects.filter(id=query)
        return finded_id
    else:
        finded_name = Product.objects.filter(name__contains=query)
        return finded_name


def search(request):
    kwargs = get_kwrgs(request)
    product_names = find(request.GET['q'])
    kwargs['product_list'] = product_names
    return render(request, 'shop/jevelry/products.html', kwargs)


class BaseView(TemplateView):
    template_name = "base.html"


class Home(View):
    template_name = "shop/index.html"

    def get(self, request, *args, **kwargs):
        kwargs = get_kwrgs(request)
        kwargs['product_list'] = Product.objects.order_by('?')[:20]
        kwargs['title'] = u'Главная'
        return render(request, self.template_name, kwargs)


class ProductDetail(View):
    model = Product
    template_name = 'shop/jevelry/product_detail.html'

    def get(self, request, *args, **kwargs):
        mykwargs = get_kwrgs(request)
        product_id = kwargs['product_id']
        product = Product.objects.get(id=product_id)
        mykwargs['product'] = product
        mykwargs['title'] = product.name
        mykwargs['form'] = CommenForm
        mykwargs['comments'] = product.comment.all()
        return render(request, self.template_name, mykwargs)

    def post(self, request, **kwargs):
        product_id = kwargs['product_id']
        formset = CommenForm(request.POST)
        if formset.is_valid():
            comment = formset.save(commit=False)
            comment.product = Product.objects.get(id=product_id)
            comment.save()
        return HttpResponseRedirect('/products/%s' % product_id)


class Checkout(TemplateView):
    template_name = 'shop/checkout.html'

    def get(self, request, *args, **kwargs):
        mykwargs = get_kwrgs(request)
        mykwargs['title'] = 'Подтверждение Заказа'
        return render(request, self.template_name, mykwargs)


class CategoryView(TemplateView):
    template_name = 'shop/jevelry/brands.html'

    def get(self, request, **kwrgs):
        mykwrgs = get_kwrgs(request)
        part_id = kwrgs['part_id']
        cat_id = kwrgs['categoty_id']
        product_list = Cat.objects.get(id=cat_id)
        product_list = product_list.brand.all()
        mykwrgs['product_list'] = product_list
        mykwrgs['title'] = Cat.objects.get(id=cat_id)
        mykwrgs['part'] = Part.objects.get(id=part_id)
        return render(request, self.template_name, mykwrgs)


class ProductView(TemplateView):
    template_name = 'shop/jevelry/products.html'

    def get(self, request, **kwrgs):
        mykwrgs = get_kwrgs(request)
        part_id = kwrgs['part_id']
        product_list = Product.objects.all()
        mykwrgs['product_list'] = product_list
        mykwrgs['compare'] = None
        mykwrgs['part'] = Part.objects.get(id=part_id)
        mykwrgs['incrustations'] = Incrustation.objects.all()
        mykwrgs['sizes'] = Size.objects.all()
        mykwrgs['brands'] = Brand.objects.all()
        mykwrgs['materials'] = Material.objects.all()
        mykwrgs['gendor'] = [x[1] for x in Product.GENDER_CHOICES]
        mykwrgs['compare_list'] = get_compare(request.session.session_key)
        response = render(request, self.template_name, mykwrgs)

        return response


def get_from_list(request, **kwargs):
        mykwrgs = get_kwrgs(request)
        part_id = kwargs['part_id']
        cat_id = kwargs['categoty_id']
        brand_id = kwargs['brand_id']
        element_id = kwargs['element_id']
        product_list = Product.objects.filter(category=cat_id)
        product_list = product_list.filter(brand=brand_id)
        product_list = product_list[element_id]
        return render(request, 'shop/jevelry/product_detail.html', mykwrgs)


class Contacts(View):
    kwargs = {}
    template_name = 'shop/contacts.html'

    def get(self, request, *args, **kwargs):
        kwargs = get_kwrgs(request)
        return render(request, self.template_name, kwargs)

    def post(self, request, *args, **kwargs):
        kwargs['cart'] = Cart(request)
        kwargs['category'] = Cat.objects.all()
        return render(request, self.template_name, kwargs)


def cart(request):
    kw = get_kwrgs(request)
    return render(request, 'shop/cart.html', kw)

def in_cart(cart, product_id):
    for i in list(cart):
        if i.product.id == int(product_id):
            return True


def add_to_cart(request):
    product_id = request.POST['product_id']
    qty = request.POST['qty']
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    if in_cart(cart, product_id):
        cart.remove(product)
        cart.add(product, product.price, qty)
    else:
        cart.add(product, product.price)
    mykwrgs = get_kwrgs(request)
    return render(request, 'shop/cart.html', mykwrgs)

def remove_from_cart(request):
    product_id = request.POST['product_id']
    kw = get_kwrgs(request)
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return render(request, 'shop/cart.html', kw)

def clear_cart(request):
    kw=get_kwrgs(request)
    cart = Cart(request)
    cart.clear()
    return render(request, 'shop/cart.html', kw)


def fresh_product(request):
    kwrgs = get_kwrgs(request)
    kwrgs['product_list'] = Product.objects.all().order_by('date_add')
    return render(request, 'shop/jevelry/parts.html', kwrgs)


class PartView(View):
    template_name = 'shop/jevelry/parts.html'

    def get(self, request, **kwrgs):
        mykwrgs = get_kwrgs(request)
        mykwrgs['product_list'] = Cat.objects.filter(part=kwrgs['part_id'])
        mykwrgs['part'] = Part.objects.get(id=kwrgs['part_id'])
        mykwrgs['title'] = mykwrgs['part']
        return render(request, self.template_name, mykwrgs)

def qs_to_json(products):
    result = {}
    for item in products:
        i = {'name': item.name,
             'id': item.id,
             'image': str(item.image)}
        result.update({item.name: i})
    return result


def choice(request):
    print 'start filter'
    for i in request.GET:
        print i
    result = Product.objects.filter(part=request.GET['part_id'])
    if 'price' in request.GET and request.GET.getlist['price'] != '':
        values = request.GET.getlist(u'price')
        result = result.filter(material__in=values)
    # if 'size[]' in request.GET:
    #     values = request.GET.getlist('size')
    #     result = result.filter(size__in=values)
    #     print 'fil size'
    if 'material' in request.GET and request.GET.getlist['material'] != '':
        values = request.GET.getlist(u'material')
        result = result.filter(material__in=values)
    return result

def sorting(request, filtered_product):
    if request.session['sort_by'] == '1':
        return filtered_product.order_by('price')
    if request.session['sort_by'] == '2':
        return filtered_product.order_by('-price')
    else:
        return filtered_product.order_by('date_add')

def add_compare(request):
    session_id = request.session.session_key
    product_id = request.GET['product_id']
    product = Product.objects.get(id=product_id)
    compare = Compare.objects.filter(session_id=session_id)
    compare_products = [x.product_id for x in compare]
    if int(product_id) not in compare_products:
        print product_id, compare_products
        obj = Compare(session_id=session_id, product=product)
        obj.save()
    return HttpResponse(json.dumps({'name': product.name, 'id': product_id}))

def get_compare(session_id):
    return Compare.objects.filter(session_id=session_id)

def get_ajax_compare(request):
    session_id = request.session.session_key
    compare_list = Compare.objects.filter(session_id=session_id)
    return render(request, 'shop/jevelry/compare_list.html', compare_list)

def do_compare(request):
    session_id = request.session.session_key
    compare_list = Compare.objects.filter(session_id=session_id)
    mykwrgs = get_kwrgs(request)
    mykwrgs['compare_list'] = compare_list
    # table = django_tables2.tables.Table(compare_list)
    return render(request, 'shop/jevelry/compare.html', mykwrgs)
    # return render_to_response('shop/jevelry/compare.html', {"table": table},)

def delete_from_compare(request, product_id):
    session_id = request.session.session_key
    compare_list = Compare.objects.filter(session_id=session_id)
    mykwrgs = get_kwrgs(request)
    product = Product.objects.get(id=product_id)
    compare = Compare.objects.filter(session_id=session_id)
    compare_products = [x.product_id for x in compare]
    if int(product_id) in compare_products:
        Compare.objects.filter(session_id=session_id, product=product).delete()
    mykwrgs['compare_list'] = compare_list
    last_url = request.META['HTTP_REFERER']
    return HttpResponseRedirect(redirect_to=last_url)
    # return render(request, 'shop/jevelry/compare.html', mykwrgs)

def ajax_products(request):
    if request.method == 'POST':
        mykwrgs = get_kwrgs(request)
        products = Product.objects.all()
        product_list = qs_to_json(products)
        data = {'html': request.POST['input']}
        data.update(product_list)
        return HttpResponse(json.dumps(data), mimetype="application/json")
    elif request.method == 'GET':
        print 'test'
        request.session['product_on_page'] = request.GET['product_on_page']
        request.session['sort_by'] = request.GET['sort_by']
        mykwrgs = get_kwrgs(request)
        filtered_product = choice(request)
        sorted_product = sorting(request, filtered_product)
        # Paginator всю задачу по делению контента на страници берет на себя
        paginator = Paginator(sorted_product, request.session['product_on_page'])
        page = request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            product_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            product_list = paginator.page(paginator.num_pages)
        mykwrgs['page_range'] = paginator.page_range
        mykwrgs['product_list'] = product_list
        mykwrgs['current_page'] = page
        mykwrgs['compare_list'] = get_compare(request.session.session_key)
        return render(request, 'shop/jevelry/products_ajax.html', mykwrgs)


def ajax_session(request):
    return HttpResponse(json.dumps({'product_on_page': request.GET['product_on_page']}))