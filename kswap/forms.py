from django import forms
from .models import Profile, Property, Booking
from django.contrib.auth.models import User


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

class PropertyBookForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ("user","property",)



class DateInput(forms.DateInput):
	input_type = 'date'

    
class PropertyBookForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        # extract user from the kwargs, and pop it to ensure it doesn't interfere with parent's __init__ method
        user = kwargs.pop('user', None)
        super(PropertyBookForm, self).__init__(*args, **kwargs)

        # filter the properties queryset by the current user
        if user:
            self.fields['my_property'].queryset = Property.objects.filter(owner=user)
        
    class Meta:
        model = Booking
        exclude = ("user", "review_text", "review_stars","property", "status")
        widgets = {
            'date_from': DateInput(),
            'date_to': DateInput(),
        }

