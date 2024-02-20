from modeltranslation.translator import TranslationOptions, register
from .models import Department


@register(Department)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
