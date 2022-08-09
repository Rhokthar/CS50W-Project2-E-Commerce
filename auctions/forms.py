from django.forms import ModelForm
from .models import *

# LISTING FORM STARTS
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        exclude = ["user"]
# LISTING FORM ENDS
