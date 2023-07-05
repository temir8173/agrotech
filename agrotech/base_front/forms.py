from django import forms
from .models import Topic, News, Services
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