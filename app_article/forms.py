from django.forms import TextInput, Textarea
from parler.forms import TranslatedField, TranslatableModelForm
from django_summernote.widgets import SummernoteWidget


# Create your forms here.


class LinkForm(TranslatableModelForm):
    name = TranslatedField(widget=TextInput(attrs={'style': 'width: 100%'}))
    link = TranslatedField(widget=TextInput(attrs={'style': 'width: 100%'}))


class ArticleForm(TranslatableModelForm):
    name = TranslatedField(widget=TextInput(attrs={'style': 'width: 100%'}))
    abstract = TranslatedField(widget=Textarea(attrs={'style': 'width: 100%', 'rows': 5}))
    content = TranslatedField(widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '600px'}}))
    