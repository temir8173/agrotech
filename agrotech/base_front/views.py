from datetime import datetime
from itertools import groupby

from django.core.paginator import Paginator
from django.db import models
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation

from agrotech import settings
from base_front.models import Topic, News, ServiceCategories, Services


def index(request: HttpRequest):
    locale = translation.get_language()

    last_events = News.objects.order_by("-publication_date").filter(locale=locale)[:4]
    current_year = datetime.now().year

    context = {
        'last_events': last_events,
        'current_year': current_year,
    }
    return render(request, "base_front/index.html", context)


def change_language(request, language_code):
    if language_code in [lang[0] for lang in settings.LANGUAGES]:
        request.session[settings.LANGUAGE_SESSION_KEY] = language_code

    previous_page = request.META.get('HTTP_REFERER')
    if previous_page:
        return redirect(previous_page)
    else:
        return redirect('/')


def investment_areas(request):
    locale = translation.get_language()

    investments = Topic.objects.order_by("id").all().filter(
        locale=locale,
        type='investment-areas',
    )

    context = {
        'investments': investments,
    }
    return render(request, "base_front/investment_areas.html", context)


def events(request):
    locale = translation.get_language()

    data_list = News.objects.all().filter(locale=locale)
    paginator = Paginator(data_list, per_page=20)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    current_year = datetime.now().year

    context = {
        'page': page,
        'current_year': current_year,
    }
    return render(request, "base_front/events/list.html", context)


def event_view(request, event_id):
    event_obj = get_object_or_404(News, id=event_id)

    context = {
        'event_obj': event_obj,
    }
    return render(request, "base_front/events/view.html", context)

def projects(request):
    locale = translation.get_language()

    agro_projects = Topic.objects.order_by("id").all().filter(
        locale=locale,
        type='projects',
    )

    context = {
        'agro_projects': agro_projects,
    }
    return render(request, "base_front/projects/list.html", context)

def project(request, project_id):
    agro_project = get_object_or_404(Topic, id=project_id)

    context = {
        'agro_project': agro_project,
    }
    return render(request, "base_front/projects/view.html", context)

def services(request):
    locale = translation.get_language()
    service_categories = ServiceCategories.objects \
        .annotate(
        name=models.F('name_' + locale),
        description=models.F('description_' + locale)
    ).values('id', 'name', 'description').all().filter()
    services_obj = Services.objects.order_by("id").all().filter(locale=locale,)
    services_by_category = {category_id: list(items) for category_id, items in
                           groupby(services_obj, key=lambda x: x.category_id)}
    categories = {item['id']: item for item in service_categories}

    context = {
        'categories': categories,
        'services_by_category': services_by_category,
    }
    return render(request, "base_front/services/list.html", context)