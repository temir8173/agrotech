from datetime import datetime
from itertools import groupby

from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation
from django.utils.translation import gettext as _


from agrotech import settings
from base_front.forms import FarmerTrainingForm
from base_front.models import Topic, News, ServiceCategories, Services, Partners, Consulting, CourseCategories, Courses


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
    locale = translation.get_language()

    try:
        event_obj = News.objects.get(id=event_id)
    except models.ObjectDoesNotExist:
        raise Http404()

    if event_obj.locale != locale:
        try:
            event_obj_translation = News.objects.get(locale=locale, base_id=event_obj.base_id)
        except models.ObjectDoesNotExist:
            raise Http404()
        return redirect('event_view', event_id=event_obj_translation.id)

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
    locale = translation.get_language()
    try:
        agro_project = Topic.objects.get(id=project_id)
    except models.ObjectDoesNotExist:
        raise Http404()

    if agro_project.locale != locale:
        try:
            agro_project_translation = Topic.objects.get(locale=locale, base_id=agro_project.base_id)
        except models.ObjectDoesNotExist:
            raise Http404()
        return redirect('project_view', project_id=agro_project_translation.id)

    context = {
        'agro_project': agro_project,
    }
    return render(request, "base_front/projects/view.html", context)

def laboratory(request):
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
    return render(request, "base_front/laboratory/list.html", context)

def partners(request):
    locale = translation.get_language()
    partners_list = Partners.objects.order_by("id").all().filter(locale=locale)

    context = {
        'partners': partners_list,
    }
    return render(request, "base_front/partners/list.html", context)

def partner(request, partner_id):
    agro_partner = get_object_or_404(Partners, id=partner_id)

    context = {
        'partner': agro_partner,
    }
    return render(request, "base_front/partners/view.html", context)

def farmer_training(request):
    if request.method == 'POST':
        form = FarmerTrainingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('training_success_submitted'))
            form = FarmerTrainingForm()
    else:
        form = FarmerTrainingForm()

    locale = translation.get_language()
    course_categories = CourseCategories.objects \
        .annotate(
        name=models.F('name_' + locale)
    ).values('id', 'name').all().filter()
    categories = {item['id']: item for item in course_categories}

    context = {
        'form': form,
        'categories': categories,
    }

    return render(request, "base_front/farmer_training.html", context)


def consulting(request):
    locale = translation.get_language()
    consulting_items = Consulting.objects.all().filter(locale=locale).order_by('name')

    context = {
        'consulting_items': consulting_items,
    }
    return render(request, "base_front/consulting/list.html", context)


def consulting_view(request, slug):
    locale = translation.get_language()
    try:
        consulting_item = Consulting.objects.get(locale=locale, slug=slug)
    except models.ObjectDoesNotExist:
        raise Http404()

    context = {
        'consulting_item': consulting_item,
    }
    return render(request, "base_front/consulting/view.html", context)


def store(request):
    locale = translation.get_language()

    context = {
        'agro_projects': 'agro_projects',
    }
    return render(request, "base_front/store/index.html", context)


def courses(request, category_id):
    locale = translation.get_language()
    courses_objects = Courses.objects.order_by("id").all().filter(category_id=category_id, locale=locale,)

    category_name = get_object_or_404(
        CourseCategories.objects.filter(id=category_id).annotate(
            name=models.F('name_' + locale)
        )
    )

    context = {
        'courses': courses_objects,
        'category_name': category_name,
    }
    return render(request, "base_front/courses/list.html", context)