from django import forms
from django.forms import ModelForm
from apps.store.models import Product, Category


class AddProductFrom(ModelForm):
    categories_query = Category.objects.filter(parentCategory__isnull=False)
    parent_category = forms.ModelChoiceField(queryset=Category.objects.filter(parentCategory__isnull=True), empty_label=None)
    category = forms.ModelChoiceField(queryset=categories_query, empty_label=None)
    name = forms.CharField(min_length=5, max_length=255, required=True)
    description = forms.CharField(required=False)
    count = forms.IntegerField(required=False, min_value=1)

    class Meta:
        model = Product
        fields = ['name', 'description', 'category']

    def __init__(self, *args, **kwargs):
        super(AddProductFrom, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({
                'id': 'categories'
            })
        self.fields['parent_category'].widget.attrs.update({
                'id': 'parent_categories'
            })
