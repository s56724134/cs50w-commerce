from django.forms import ModelForm
from .models import Listing

class AuctionListingForm(ModelForm):
    class Meta:
        model = Listing
        labels = {"image": "Pictures (optional)"}
        fields = ["title", "description", "starting_bid", "category", "image"]
        