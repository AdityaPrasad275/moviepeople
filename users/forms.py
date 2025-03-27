from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["role", "location", "bio"]


class UserSearchForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, required=False)
    role = forms.CharField(label="Role", max_length=100, required=False)
    location = forms.CharField(label="Location", max_length=100, required=False)
