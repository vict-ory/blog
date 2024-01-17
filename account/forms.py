from django import forms
from account.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name','first_name','mobile','passport',]