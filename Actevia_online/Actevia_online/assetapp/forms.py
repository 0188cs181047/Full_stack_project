from django import forms
from .models import Asset_inform
from django.db.models import Q

class AssetInformForm(forms.ModelForm):
    class Meta:
        model = Asset_inform
        fields = ['asset_id', 'asset_photo', 'asset_owner', 'asset_type','asset_status']
        labels = {
            'asset_id': 'Asset ID',
            'asset_photo': 'Asset Photo',
            'asset_owner': 'Asset Owner',
            'asset_type': 'Asset Type',
            'asset_status' : 'Asset Status',
        }
        widgets = {
            'asset_photo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class AssetFilterForm(forms.Form):
    asset_id = forms.CharField(required=False)
    asset_owner = forms.CharField(required=False)
    asset_type = forms.CharField(required=False)
    asset_status = forms.CharField(required=False)




    
