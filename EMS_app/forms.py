from django import forms
# from django.core.exceptions import ValidationError
# from django.core.validators import RegexValidator
from .models import Organizer

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True,
                               min_length=5)
    email = forms.EmailField(max_length=50, required=True)

    #first_name = forms.CharField(max_length=30, required=True, validators=[
     #   RegexValidator(r'^[a-zA-Z]*$', message="First name should not contain numerics, only alphabets")])
    #last_name = forms.CharField(max_length=30, required=True, validators=[
       # RegexValidator(r'^[a-zA-Z]*$', message="Last name should not contain numerics, only alphabets")])

    gender = forms.ChoiceField(
        choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
        widget=forms.RadioSelect(),
        required=True,
    )
    phone_number = forms.IntegerField(required = True)
    role = forms.ChoiceField(
        choices=(("Organizer", "Organizer"), ("Participant", "Participant")),
        widget=forms.RadioSelect(),
        required=True,
    )


class EventForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    location = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    start_date = forms.DateTimeField(required=True, input_formats=['%Y-%m-%d %H:%M:%S'])
    end_date = forms.DateTimeField(required=True, input_formats=['%Y-%m-%d %H:%M:%S'])
    #org_id = forms.ModelChoiceField(queryset=Organizer.objects.all(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        # Check if start_date is before end_date
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("End date should be after start date.")