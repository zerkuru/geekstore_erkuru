from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import ProductCategory, Product
import random
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import never_cache


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu',
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}',
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}',
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products',
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True, quantity__gte=1).select_related(
                'category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True, quantity__gte=1).select_related(
            'category')


def get_products_order_by_price():
    if settings.LOW_CACHE:
        key = 'products',
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True, quantity__gte=1).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True, quantity__gte=1).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True,
                                              category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True,
                                      category__is_active=True).order_by('price')


def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


@never_cache
def products(request, pk=None, page=1):
    title = 'Каталог'

    links_menu = get_links_menu()

    if pk is not None:
        if pk == 0:
            category = {'pk': 0, 'name': 'все'}
            products = get_products_in_category_orederd_by_price(pk)
        else:
            category = get_category(pk)
            products = get_products_in_category_orederd_by_price(pk)

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
        }
        return render(request, 'mainapp/products.html', context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    products = get_products_order_by_price()

    context = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        'products': products,
    }

    return render(request, 'mainapp/products.html', context)


@never_cache
def product(request, pk):
    title = 'Детали'

    product = get_product(pk)

    context = {
        'title': title,
        'links_menu': get_links_menu(),
        'product': product,
        'same_products': get_same_products(product),
    }
    return render(request, 'mainapp/product.html', context)
