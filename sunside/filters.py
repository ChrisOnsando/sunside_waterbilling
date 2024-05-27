import django_filters
from django_filters import CharFilter
from django import forms
from .models import *

class CategoryFilter(django_filters.FilterSet):
    name = CharFilter(field_name="name", label="Name", lookup_expr="icontains", widget=forms.TextInput(attrs={'class': 'form-control mt-1 col-lg-3', 'placeholder': 'Enter Category'}))

    class Meta:
        model = Category
        fields = ('name', 'status')
        labels = {
            'name' : 'Name',
            'status': 'Status',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.form.fields:
            self.form.fields[field_name].widget.attrs.update({'class': 'form-control mt-1 col-lg-3'})
            