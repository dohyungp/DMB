from django import forms
from .models import Profile
from pagedown.widgets import PagedownWidget


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=PagedownWidget(show_preview=False), label="자기소개")
    class Meta:
        model = Profile
        fields = [
            'avatar',
            'bio',
        ]