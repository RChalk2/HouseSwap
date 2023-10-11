from django import forms
from .models import Profile, Property


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ("user",)


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        # exclude owner so that the user cannot choose it from all users.  Rather the function above ensures that the owner is the user
        exclude = (
            "id",
            "owner",
        )
