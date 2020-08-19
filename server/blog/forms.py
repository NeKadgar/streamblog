from django import forms
from .models import Image
from taggit.forms import *


class MyForm(forms.Form):
    name = forms.CharField()
    m_tags = TagField()

