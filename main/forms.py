from django.forms import ModelForm
from .models import User, FavouriteCatagory, Reveaws
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model= User
        fields= ['name','email','phone', 'password1', 'password2']



class UserEditForm(ModelForm):
	class Meta:
		model= User
		fields= ['name','username','email','phone']


class FavouriteForm(ModelForm):
    class Meta:
        model= FavouriteCatagory
        fields= ['catagory']


# class ReveawForm(ModelForm):
# 	class Meta:
# 		model= Reveaws
# 		fields= ['taitle', 'body']