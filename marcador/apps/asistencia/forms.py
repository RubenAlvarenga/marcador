from django.forms import ModelForm
from django.contrib.auth.models import User, Group, Permission
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import FilteredSelectMultiple, ForeignKeyRawIdWidget

class UserForm(UserCreationForm):
    GRUPO=(
        ('empleado', 'Empleado'),
        ('empleador', 'Empleador'), 
        ('administrador', 'Administrador')
    )
    grupo = forms.ChoiceField(choices=GRUPO, widget=forms.Select(attrs={'class':'form-control'}))
    nombre = forms.CharField(required = True, widget=forms.TextInput(attrs = {'class':'form-control'}))
    apellido = forms.CharField(required = True, widget=forms.TextInput(attrs = {'class':'form-control'}))
    password1 = forms.CharField(required = True, widget=forms.PasswordInput(attrs = {'class':'form-control'}))
    password2 = forms.CharField(required = True, widget=forms.PasswordInput(attrs = {'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'nombre', 'apellido', 'email']
        widgets = {
            'username' : forms.TextInput(attrs = {'class':'form-control'}),
            'email': forms.TextInput(attrs = {'class':'form-control'}),
        }
    def clean_first_name(self):
        return self.cleaned_data['first_name'].capitalize()
    def clean_last_name(self):
        return self.cleaned_data['last_name'].capitalize()






class updUserForm(ModelForm):
    GRUPO=(
        ('empleado', 'Empleado'),
        ('empleador', 'Empleador'), 
        ('administrador', 'Administrador')
    )
    grupo = forms.ChoiceField(choices=GRUPO, widget=forms.Select(attrs={'class':'form-control'}))


    email = forms.EmailField(required = False, widget=forms.TextInput(attrs = {'class':'form-control'}))
    first_name = forms.CharField(label='Nombre', required = True, widget=forms.TextInput(attrs = {'class':'form-control'}))
    last_name = forms.CharField(label='Apellido', required = True, widget=forms.TextInput(attrs = {'class':'form-control'}))

    class Meta:
        model = User
        exclude = ['is_superuser', 'last_login', 'date_joined', 'is_staff', 'password']
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active')
        widgets = {
            'username' : forms.TextInput(attrs = {'class':'form-control'}),
            'first_name' : forms.TextInput(attrs = {'class':'form-control'}),
            'last_name' : forms.TextInput(attrs = {'class':'form-control'}),
        }
    def clean_first_name(self):
        return self.cleaned_data['first_name'].capitalize()
    def clean_last_name(self):
        return self.cleaned_data['last_name'].capitalize()
