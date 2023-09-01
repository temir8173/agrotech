from django.db import models
from django.utils.translation import gettext as _

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
    base_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    publication_date = models.DateField()
    image = models.ImageField(upload_to='news_images/')
    locale = models.CharField(max_length=4, default='kk', choices=settings.LANGUAGES)

    class Meta:
        verbose_name_plural = "News"


class ServiceCategories(models.Model):
    name_kk = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    description_kk = models.TextField(max_length=255, null=True, blank=True)
    description_ru = models.TextField(max_length=255, null=True, blank=True)
    description_en = models.TextField(max_length=255, null=True, blank=True)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name_ru


class Services(models.Model):
    base_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    locale = models.CharField(max_length=4, default='kk', choices=settings.LANGUAGES)
    description = models.TextField(max_length=255, null=True, blank=True)
    price = models.CharField(max_length=64)
    category = models.ForeignKey(ServiceCategories, on_delete=models.CASCADE, null=True, default=None)

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
