from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if not email:
            self.add_error('email', forms.ValidationError("Email is required."))

        if email and User.objects.filter(email=email).exists():
            self.add_error('email', forms.ValidationError("Email is already in use."))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True

        if commit:
            user.save()

        return user


class AddCategory(forms.ModelForm):
  name=models.CharField(max_length=350,blank=True, null=True)
  status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)

  class Meta:
        model = Category
        fields = ('name','status')
        labels = {
            'name': 'Category Name',
            'status': 'Status',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class':'form-control'}),
        }




class EditCategory(forms.ModelForm):
    name=models.CharField(max_length=350,blank=True, null=True)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)

    class Meta:
        model = Category
        fields = ('name','status')
        labels = {
            'name': 'Category Name',
            'status': 'Status',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class':'form-control'}),
        }

class AddClient(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['category', 'first_name', 'middle_name', 'last_name', 'contact', 'address', 'meter_code', 'first_reading', 'status']
        labels = {
            'category': 'Category',
            'first_name': 'First Name',
            'middle_name': 'Middle Name',
            'last_name': 'Last Name',
            'contact': 'Contact',
            'address': 'Address',
            'meter_code': 'Meter Code',
            'first_reading': 'First Reading',
            'status': 'Status',
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'meter_code': forms.TextInput(attrs={'class': 'form-control'}),
            'first_reading': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class EditClient(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['category', 'first_name', 'middle_name', 'last_name', 'contact', 'address', 'meter_code', 'first_reading', 'status']
        labels = {
            'category': 'Category',
            'first_name': 'First Name',
            'middle_name': 'Middle Name',
            'last_name': 'Last Name',
            'contact': 'Contact',
            'address': 'Address',
            'meter_code': 'Meter Code',
            'first_reading': 'First Reading',
            'status': 'Status',
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'meter_code': forms.TextInput(attrs={'class': 'form-control'}),
            'first_reading': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        