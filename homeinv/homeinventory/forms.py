from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Location
from .models import Asset
from .models import Service

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
	
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class LoginForm(forms.Form):
	username = forms.CharField(max_length=20)
	password = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=20)
	class Meta:
		model = User
		fields = ['username', 'password']
		
		
class LocationForm(ModelForm):
	class Meta:
			model = Location
			fields = ['id','name', 'address', 'locationType']
	
class AssetForm(ModelForm):
	class Meta:
			model = Asset
			fields = ['id', 'location', 'name', 'assettype','serial','purchasedate','price','document']


class ServiceForm(ModelForm):
	class Meta:
			model = Service
			fields = ['id', 'location', 'servicename', 'provider','clientno','purchasedate','document']
