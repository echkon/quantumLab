# In users/forms.py
from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']  # Include first_name and last_name fields

    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']

        if password != password_confirm:
            raise forms.ValidationError('Passwords do not match')
        return password_confirm
    
    def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password'])  # Hash the password!
            if commit:
                user.save()
            return user