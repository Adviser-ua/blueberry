# -*- coding: UTF-8 -*-
__author__ = 'Konstantyn Davidenko'

from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'^$', Home.as_view()),
    url(r'^(?P<part_id>[0-9])/$', ProductView.as_view()),
    url(r'^(?P<part_id>[0-9])/(?P<categoty_id>[0-9])/(?P<brand_id>[0-9])/(?P<product_id>[0-9])/$', ProductDetail.as_view()),
    # url(r'^(?P<part_id>[0-9])/(?P<categoty_id>[0-9])/(?P<brand_id>[0-9])/(?P<product_id>[0-9])/(?P<element_id>[0-9])/$', get_from_list),
    url(r'^test$', BaseView.as_view()),
    url(r'^products/(?P<product_id>\d+)/$', ProductDetail.as_view()),
    url(r'^checkout/$', Checkout.as_view()),
    url(r'^contacts/$', Contacts.as_view()),
    url(r'^cart/$', cart),
    url(r'^add_to_cart/$', add_to_cart),
    url(r'^remove_from_cart/$', remove_from_cart),
    url(r'^clear_cart/$', clear_cart),
    url(r'^login', Login.as_view()),
    url(r'^logout', Logout.as_view()),
    url(r'^search/', search),
    url(r'^last_product/', fresh_product),
    url(r'^register/', Register.as_view()),
    url(r'^user_account/', UserAccount.as_view()),
    url(r'^register/$', Register.as_view()),
    url(r'^ajax/$', ajax_products),
    url(r'^ajax_session/$', ajax_session),
    url(r'^add_compare/$', add_compare),
    url(r'^delete_from_compare/(?P<product_id>[0-9])$', delete_from_compare),
    url(r'^get_compare/$', get_ajax_compare),
    url(r'^compare/$', do_compare),

)