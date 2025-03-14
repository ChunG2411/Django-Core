from django.forms import TextInput, Textarea
from parler.forms import TranslatedField, TranslatableModelForm
from django_summernote.widgets import SummernoteWidget


# Create your forms here.


class APIKeyForm(TranslatableModelForm):
    name = TranslatedField(widget=TextInput(attrs={'style': 'width: 100%'}))
    des = TranslatedField(widget=Textarea(attrs={'style': 'width: 100%', 'rows': 5}))
    