from django.shortcuts import render

from mainapp.models import ProductCategory


def main(request):
    return render(request, 'mainapp/index.html')
    


def contact(request):
    return render(request, 'mainapp/contact.html')

def products(request):
    title = 'Каталог'

    links_menu = ProductCategory.objects.all()
    context = {
        'title': title,
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', context)


from .models import ProductCategory, Product


def main(request):
    title = 'главная'

    products = Product.objects.all()[:4]

    content = {'title': title, 'products': products}
    return render(request, 'mainapp/index.html', content)