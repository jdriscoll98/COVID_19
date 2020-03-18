from django import forms
from apps.subscribers.models import Subscriber
import phonenumbers

class SubscriberForm(forms.Form):
    telephone = forms.CharField(max_length=100)

    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        parsed_number = phonenumbers.parse(telephone, "US")
        number = f"+{parsed_number.country_code}{parsed_number.national_number}"
        if Subscriber.objects.filter(telephone=number).exists():
            raise forms.ValidationError("Error, number already registered.")
        return telephone