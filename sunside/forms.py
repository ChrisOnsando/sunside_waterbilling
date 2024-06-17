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

class BillForm(forms.ModelForm):
    previous_reading = forms.DecimalField(disabled=True, label='Previous Reading', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    total_bill = forms.DecimalField(disabled=True, label='Total Bill', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Bill
        fields = ['client', 'reading_date', 'current_reading', 'due_date', 'status']
        labels = {
            'client': 'Client',
            'reading_date': 'Reading Date',
            'current_reading': 'Current Reading',
            'due_date': 'Due Date',
            'status': 'Status',
        }
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'reading_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'current_reading': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(BillForm, self).__init__(*args, **kwargs)
        if 'client' in self.data:
            try:
                client_id = int(self.data.get('client'))
                client = Client.objects.get(id=client_id)
                last_bill = Bill.objects.filter(client=client).order_by('-reading_date').first()
                previous_reading = last_bill.current_reading if last_bill else client.first_reading
                self.fields['previous_reading'].initial = previous_reading
            except (ValueError, TypeError, Client.DoesNotExist):
                self.fields['previous_reading'].initial = 0.00
        else:
            self.fields['previous_reading'].initial = 0.00

        self.fields['total_bill'].initial = 0.00  # Initialize total_bill to 0.00

    def clean(self):
        cleaned_data = super().clean()
        client = cleaned_data.get('client')
        current_reading = cleaned_data.get('current_reading')
        
        if client and current_reading is not None:
            last_bill = Bill.objects.filter(client=client).order_by('-reading_date').first()
            previous_reading = last_bill.current_reading if last_bill else client.first_reading
            cleaned_data['previous_reading'] = previous_reading
            cleaned_data['total_bill'] = (current_reading - previous_reading) * 30
        return cleaned_data

class BillEditForm(forms.ModelForm):
    previous_reading = forms.DecimalField(disabled=True, label='Previous Reading', widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    total_bill = forms.DecimalField(disabled=True, label='Total Bill', widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    class Meta:
        model = Bill
        fields = ['client', 'reading_date', 'current_reading', 'due_date', 'status']
        labels = {
            'client': 'Client',
            'reading_date': 'Reading Date',
            'current_reading': 'Current Reading',
            'due_date': 'Due Date',
            'status': 'Status',
        }
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'reading_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'readonly': 'readonly'}),
            'current_reading': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'readonly': 'readonly'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(BillEditForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['previous_reading'].initial = instance.previous_reading
            self.fields['total_bill'].initial = instance.total_bill

    def clean(self):
        cleaned_data = super().clean()
        client = cleaned_data.get('client')
        current_reading = cleaned_data.get('current_reading')
        
        if client and current_reading is not None:
            last_bill = Bill.objects.filter(client=client).order_by('-reading_date').exclude(pk=self.instance.pk).first()
            previous_reading = last_bill.current_reading if last_bill else client.first_reading
            cleaned_data['previous_reading'] = previous_reading
            cleaned_data['total_bill'] = (current_reading - previous_reading) * 30
        return cleaned_data

