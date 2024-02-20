from django.db import models
from django.utils.translation import gettext as _
from django.utils.text import slugify
from transliterate import translit

from agrotech import settings


class Topic(models.Model):
    TYPES = [
        ('investment-areas', 'Инвестиционные направления'),
        ('projects', 'Проекты'),
    ]
    base_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=32, choices=TYPES)
    description = models.TextField()
    locale = models.CharField(max_length=4, default='kk', choices=settings.LANGUAGES)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__} #{self.pk} {self.name!r}>"


class News(models.Model):
    TYPES = [
        ('event', 'Event'),
        ('new', 'New'),
    ]
    base_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255)
    type = models.CharField(
        max_length=10,
        choices=TYPES,
        default='event'
    )
    content = models.TextField()
    publication_date = models.DateField()
    image = models.ImageField(upload_to='news_images/')
    locale = models.CharField(max_length=4, default='kk', choices=settings.LANGUAGES)
    views = models.IntegerField(null=True, blank=True, default=1)

    class Meta:
        verbose_name_plural = "News"


class Department(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, default='', blank=True)
    description = models.TextField(null=True, blank=True)
    contact_phone = models.CharField(max_length=255, null=True, default='')

    @classmethod
    def departments_with_services(cls):
        departments_with_services = {'/service/consulting': _('menu_consulting'),}
        departments = cls.objects.filter(servicecategories__isnull=False).distinct()
        for department in departments:
            if department.slug and department.name:
                departments_with_services['/service/' + department.slug] = _(department.name)

        return departments_with_services

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name


class ServiceCategories(models.Model):
    name_kk = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    description_kk = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)
    contact_phone = models.CharField(max_length=255, blank=True, null=True, default='')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, default=None)

    @classmethod
    def get_service_categories(cls, locale, department_id):
        # Annotate and filter the queryset
        service_categories = cls.objects \
            .annotate(
            name=models.Case(
                models.When(**{'name_' + locale: ''}, then='name_en'),
                default='name_' + locale,
                output_field=models.CharField()
            ),
            description=models.Case(
                models.When(**{'description_' + locale: ''}, then='description_en'),
                default='description_' + locale,
                output_field=models.CharField()
            )
        ) \
            .values('id', 'name', 'description') \
            .filter(department_id=department_id)

        return service_categories

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name_ru


class Services(models.Model):
    base_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    locale = models.CharField(max_length=4, default='kk', choices=settings.LANGUAGES)
    description = models.TextField(null=True, blank=True)
    price = models.CharField(max_length=64)
    category = models.ForeignKey(ServiceCategories, on_delete=models.CASCADE, null=True, default=None)
    contact_phone = models.CharField(max_length=255, blank=True, null=True, default='')

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name


class Partners(models.Model):
    base_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(upload_to='partners_logo/')
    locale = models.CharField(max_length=4, default='kk', choices=settings.LANGUAGES)
    description = models.TextField(max_length=1500, null=True, blank=True)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name


class Consulting(models.Model):
    base_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=True, blank=True)
    locale = models.CharField(max_length=4, default='kk', choices=settings.LANGUAGES)
    logo = models.ImageField(upload_to='consulting_logo/', null=True, blank=True)
    description = models.TextField(max_length=1500, null=True, blank=True)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name

class TrainingRequests(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    question = models.TextField(max_length=1500, null=True, blank=True)
    is_answered = models.BooleanField(default=False)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name


class CourseCategories(models.Model):
    name_kk = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name_ru

class Courses(models.Model):
    base_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    locale = models.CharField(max_length=4, default='kk', choices=settings.LANGUAGES)
    description = models.TextField(max_length=10000, null=True, blank=True)
    category = models.ForeignKey(CourseCategories, on_delete=models.CASCADE, null=True, default=None)
    price = models.IntegerField(null=True, blank=True)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name


class ProductCategories(models.Model):
    name_kk = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name_ru


class ProductSeller(models.Model):
    name_kk = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=255, null=True, default='')

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name_ru


class Products(models.Model):
    base_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    locale = models.CharField(max_length=4, default='kk', choices=settings.LANGUAGES)
    variety = models.CharField(max_length=255, null=True, blank=True)
    reproduction = models.CharField(max_length=255, null=True, blank=True)
    price = models.CharField(max_length=64)
    category = models.ForeignKey(ProductCategories, on_delete=models.CASCADE, null=True, default=None)
    seller = models.ForeignKey(ProductSeller, on_delete=models.CASCADE, null=True, default=None)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name

    def __get_label(self, field):
        return self._meta.get_field(field).verbose_name

    def __get_help_text(self, field):
        return self._meta.get_field(field).help_text

    @property
    def name_label(self):
        return _('product_name_label')

    @property
    def variety_label(self):
        return _('product_variety_label')

    @property
    def reproduction_label(self):
        return _('product_reproduction_label')

    @property
    def price_label(self):
        return _('product_price_label')
