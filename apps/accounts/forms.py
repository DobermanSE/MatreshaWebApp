from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Пользователь с таким email уже существует')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.firstname = self.cleaned_data["firstname"]
        user.lastname = self.cleaned_data["lastname"]
        if commit:
            user.is_active = False
            user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class CustomerRegistrationForm(RegistrationForm):
    firstname = forms.CharField(required=True)
    lastname = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'username')


class SellerRegistrationForm(RegistrationForm):
    firstname = forms.CharField(required=False)
    lastname = forms.CharField(required=False)
    company_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('company_name', 'firstname', 'lastname', 'username')
