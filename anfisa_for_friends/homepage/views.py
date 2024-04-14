from django.db.models import Q
from django.shortcuts import render
from ice_cream.models import IceCream


def index(request):
    template = 'homepage/index.html'
    ice_cream_list_q = IceCream.objects.values(
        'title', 'id', 'description', 'category__title', 'category__slug'
    ).filter(
        (Q(is_on_main=True) & Q(is_published=True))
        | (Q(title__contains='пломбир') & Q(is_published=True))
    ).order_by('title')[1:4]
    ice_cream_list_values_filtration = IceCream.objects.values(
        'id', 'title', 'category__title'
    ).filter(
        category__is_published=True
    )
    ice_cream_list_related_filtration = IceCream.objects.select_related(
        'category'
    ).filter(
        category__is_published=True
    )
    ice_cream_list = IceCream.objects.values(
        'id', 'title', 'price', 'description'
    ).filter(
        # Проверяем, что
        is_published=True,  # Сорт разрешён к публикации;
        is_on_main=True,  # Сорт разрешён к публикации на главной странице;
        category__is_published=True  # Категория разрешена к публикации.
    )
    context = {
        'ice_cream_list': ice_cream_list,
    }
    return render(request, template, context)
