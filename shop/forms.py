# -*- coding: UTF-8 -*-
__author__ = 'Konstantyn Davidenko'

from django.forms import Form, ModelForm
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from models import Comment
from django import forms
import django_filters

class MyForm(Form):
    pass


class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


class CommenForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'comment']

from .models import Product


class MyFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(MyFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = Product
        fields = {'price',
                  'incrustation',
                  'brand',
                  'material',
                  'size',
                  'availability'
                 }

class UserlistForm(Form):
    users = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label="Notify and subscribe users to this post:")