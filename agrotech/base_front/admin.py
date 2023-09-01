from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.db import models

from agrotech.settings import LANGUAGES
from .forms import TopicForm, NewsForm, ServicesForm, PartnersForm, FarmerTrainingForm
from .models import Topic, News, Services, ServiceCategories, Partners, Consulting, TrainingRequests


class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.base_id is None:
            obj.base_id = obj.id

        super().save_model(request, obj, form, change)

    def translate_links_common(self, obj, model: models.Model):
        translations = {}
        for code, name in LANGUAGES:
            if code != obj.locale:
                translation = model.objects.values('id').filter(base_id=(obj.base_id or obj.id), locale=code).first()
                if translation is not None and 'id' in translation:
                    translations[code] = translation['id']
                else:
                    translations[code] = False

        return translations


@admin.register(Topic)
class TopicAdmin(BaseModelAdmin):
    form = TopicForm
    # readonly_fields = ('base_id',)
    fields = ('base_id', 'name', 'type', 'locale', 'description',)
    list_display = ['name', 'type', 'locale', 'translate_links', 'get_short_descr']
    list_filter = ('type', 'locale', )
    search_fields = ('name__startswith', 'description')

    def get_short_descr(self, obj):
        if len(obj.description) > 100:
            return obj.description[:100] + '...'
        return obj.description

    get_short_descr.short_description = 'Description'

    def translate_links(self, obj):
        model = Topic
        translations = self.translate_links_common(obj, model)
        links = ''
        for lang_code, translation_id in translations.items():
            if translation_id:
                url = reverse('admin:base_front_topic_change', args=(translation_id,))
            else:
                url = (
                    reverse('admin:base_front_topic_add')
                    + "?" + urlencode({'base_id': f"{obj.base_id}"})
                    + "&" + urlencode({'type': f"{obj.type}"})
                    + "&" + urlencode({'locale': f"{lang_code}"})
                )
            links += format_html('<a href="{}">{}</a> ', url, lang_code)

        return mark_safe(links)


@admin.register(News)
class NewsAdmin(BaseModelAdmin):
    verbose_name_plural = 'News'

    form = NewsForm
    fields = ('base_id', 'title', 'publication_date', 'image', 'locale', 'content')
    list_display = ['title', 'publication_date', 'locale', 'get_short_content', 'translate_links']
    list_filter = ('locale', )
    search_fields = ('name__startswith', 'description')

    def get_short_content(self, obj):
        if len(obj.content) > 100:
            return obj.content[:100] + '...'
        return obj.content

    get_short_content.short_description = 'Content'

    def translate_links(self, obj):
        model = News
        translations = self.translate_links_common(obj, model)
        links = ''
        for lang_code, translation_id in translations.items():
            if translation_id:
                url = reverse('admin:base_front_news_change', args=(translation_id,))
            else:
                url = (
                    reverse('admin:base_front_news_add')
                    + "?" + urlencode({'base_id': f"{obj.base_id}"})
                    + "&" + urlencode({'locale': f"{lang_code}"})
                )
            links += format_html('<a href="{}">{}</a> ', url, lang_code)

        return mark_safe(links)


@admin.register(Services)
class ServicesAdmin(BaseModelAdmin):
    verbose_name_plural = 'Service'

    form = ServicesForm
    fields = ('base_id', 'name', 'locale', 'price', 'category', 'description')
    list_display = ['name', 'locale', 'translate_links', 'price', 'category', 'description']
    list_filter = ('locale', )
    search_fields = ('name__startswith', 'description')

    def translate_links(self, obj):
        model = Services
        translations = self.translate_links_common(obj, model)
        links = ''
        for lang_code, translation_id in translations.items():
            if translation_id:
                url = reverse('admin:base_front_services_change', args=(translation_id,))
            else:
                url = (
                    reverse('admin:base_front_services_add')
                    + "?" + urlencode({'base_id': f"{obj.base_id}"})
                    + "&" + urlencode({'category': f"{obj.category}"})
                    + "&" + urlencode({'locale': f"{lang_code}"})
                )
            links += format_html('<a href="{}">{}</a> ', url, lang_code)

        return mark_safe(links)


@admin.register(ServiceCategories)
class ServiceCategoriesAdmin(admin.ModelAdmin):
    fields = ('name_kk', 'name_ru', 'name_en', 'description_kk', 'description_ru', 'description_en')
    list_display = ['name_kk', 'name_ru', 'name_en', 'description_kk', 'description_ru', 'description_en']


@admin.register(Partners)
class PartnersAdmin(BaseModelAdmin):
    verbose_name_plural = 'Partner'

    form = PartnersForm
    fields = ('base_id', 'name', 'link', 'logo', 'locale', 'description')
    list_display = ['name', 'locale', 'link', 'translate_links', 'logo', 'get_short_descr']

    def translate_links(self, obj):
        model = Partners
        translations = self.translate_links_common(obj, model)
        links = ''
        for lang_code, translation_id in translations.items():
            if translation_id:
                url = reverse('admin:base_front_partners_change', args=(translation_id,))
            else:
                url = (
                    reverse('admin:base_front_partners_add')
                    + "?" + urlencode({'base_id': f"{obj.base_id}"})
                    + "&" + urlencode({'locale': f"{lang_code}"})
                )
            links += format_html('<a href="{}">{}</a> ', url, lang_code)

        return mark_safe(links)

    def get_short_descr(self, obj):
        if len(obj.description) > 100:
            return obj.description[:100] + '...'
        return obj.description


@admin.register(Consulting)
class ConsultingAdmin(BaseModelAdmin):
    form = PartnersForm
    fields = ('base_id', 'name', 'slug', 'logo', 'locale', 'description')
    list_display = ['name', 'locale', 'slug', 'translate_links', 'logo', 'get_short_descr']

    def translate_links(self, obj):
        model = Consulting
        translations = self.translate_links_common(obj, model)
        links = ''
        for lang_code, translation_id in translations.items():
            if translation_id:
                url = reverse('admin:base_front_consulting_change', args=(translation_id,))
            else:
                url = (
                    reverse('admin:base_front_consulting_add')
                    + "?" + urlencode({'base_id': f"{obj.base_id}"})
                    + "&" + urlencode({'locale': f"{lang_code}"})
                    + "&" + urlencode({'slug': f"{obj.slug}"})
                    + "&" + urlencode({'logo': f"{obj.logo}"})
                )
            links += format_html('<a href="{}">{}</a> ', url, lang_code)

        return mark_safe(links)

    def get_short_descr(self, obj):
        if len(obj.description) > 100:
            return obj.description[:100] + '...'
        return obj.description


@admin.register(TrainingRequests)
class TrainingRequestsAdmin(admin.ModelAdmin):
    form = FarmerTrainingForm

    # fields = ('base_id', 'name', 'slug', 'logo', 'locale', 'description')
    list_display = ['name', 'email', 'phone', 'question', 'is_answered']