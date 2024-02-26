from django import forms
from .models import Asset_inform
from django.db.models import Q

class AssetInformForm(forms.ModelForm):
    Asset_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Asset Date', 'type': 'date'})
    )
    class Meta:
        model = Asset_inform
        fields = ['email','asset_id', 'asset_owner', 'asset_type','asset_status','Asset_date']
        labels = {
            'email': 'Email',
            'asset_id': 'Asset ID',
            'asset_owner': 'Asset Owner',
            'asset_type': 'Asset Type',
            'asset_status' : 'Asset Status',
            'Asset_date': 'Asset Date',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'asset_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asset ID'}),
            'asset_owner': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asset Owner'}),
            'asset_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asset Type'}),
        }


class UpdateAssetForm(forms.ModelForm):
    Asset_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Asset_inform
        fields = ['email','asset_owner', 'asset_type', 'asset_status','Asset_date']
        labels = {
            'email': 'Email',
            'asset_owner': 'Asset Owner',
            'asset_type': 'Asset Type',
            'asset_status': 'Asset Status',
            'Asset_date': 'Asset Date',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'asset_owner': forms.TextInput(attrs={'class': 'form-control'}),
            'asset_type': forms.TextInput(attrs={'class': 'form-control'}),
            'asset_status': forms.Select(attrs={'class': 'form-control'}),
        }




class AssetFilterForm(forms.Form):
    asset_filter = forms.CharField(
        label="Filter Assets",
        widget=forms.TextInput(attrs={
            'id': 'asset-filter',
            'placeholder': 'Search by ID, owner, type, or status',
        }),
        required=False,
    )

    def filter_queryset(self, queryset):
        asset_filter = self.cleaned_data.get('asset_filter')
        if asset_filter:
            queryset = queryset.filter(
                Q(asset_id__icontains=asset_filter) |
                Q(asset_owner__icontains=asset_filter) |
                Q(asset_type__icontains=asset_filter) |
                Q(asset_status__icontains=asset_filter) 
            )
        return queryset
    
