from django import forms
from main.models import Product, Blog, FlashDeal, CoverSell, TrendCover, FeaturedProduct
from ckeditor.widgets import CKEditorWidget

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProductForm(forms.ModelForm):
    images = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'multiple': True
        })
    )
    
    class Meta:
        model = Product
        fields = ['taitle', 'catagory', 'price', 'WasPrice', 'DeleveryPrice', 'dicription', 'info']
        widgets = {
            'taitle': forms.TextInput(attrs={'class': 'form-control'}),
            'catagory': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'WasPrice': forms.TextInput(attrs={'class': 'form-control'}),
            'DeleveryPrice': forms.TextInput(attrs={'class': 'form-control'}),
            'size': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dicription': forms.Textarea(attrs={'class': 'form-control'}),
            'info': forms.Textarea(attrs={'class': 'form-control'}),
        }

class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'id_content'}))
    
    class Meta:
        model = Blog
        fields = ['title', 'content', 'featured_image', 'excerpt', 'category', 'tags', 'is_published']
        widgets = {
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select', 'multiple': True}),
            'is_published': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
        }

from main.models import CoverSell, TrendCover, FeaturedProduct
# --- CoverSell Form ---
class CoverSellForm(forms.ModelForm):
    class Meta:
        model = CoverSell
        fields = ['image', 'mobile_image', 'url']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'mobile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
        }

# --- TrendCover Form ---
class TrendCoverForm(forms.ModelForm):
    class Meta:
        model = TrendCover
        fields = ['link', 'image']
        widgets = {
            'link': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

# --- FlashDeal Form ---
class FlashDealForm(forms.ModelForm):
    class Meta:
        model = FlashDeal
        fields = ['taitle', 'image', 'price', 'url', 'background']
        widgets = {
            'taitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Flash Deal Title'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price (e.g., 50% OFF)'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link to product or section'}),
            'background': forms.FileInput(attrs={'class': 'form-control'}),
        }

# --- FeaturedProduct Form ---
class FeaturedProductForm(forms.ModelForm):
    class Meta:
        model = FeaturedProduct
        fields = ['background', 'catagory', 'taitle', 'url']
        widgets = {
            'background': forms.FileInput(attrs={'class': 'form-control'}),
            'catagory': forms.Select(attrs={'class': 'form-control'}),
            'taitle': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
        }