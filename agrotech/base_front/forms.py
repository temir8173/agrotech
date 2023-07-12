from django import forms
from .models import Topic, News, Services, Partners, Consulting
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingFormField

class TopicForm(forms.ModelForm):
    description = RichTextUploadingFormField(widget=CKEditorWidget())

    class Meta:
        model = Topic
        fields = '__all__'

class NewsForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = News
        fields = '__all__'


class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'


class PartnersForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Partners
        fields = '__all__'


class ConsultingForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Consulting
        fields = '__all__'


class FarmerTrainingForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    message = forms.CharField(label='My Textarea Field', widget=forms.Textarea)