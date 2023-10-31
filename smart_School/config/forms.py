from django import forms

from .models import Config

class ConfigForm(forms.ModelForm):
    class Meta:
        model=Config
        fields='__all__'
    time_start_working=forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type':'time'}))
    num_hour_working=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    url_extract_data=forms.URLField(widget=forms.URLInput(attrs={'class':'form-control','placeholder':'https://www.example.com'}))
    url_image=forms.URLField(widget=forms.URLInput(attrs={'class':'form-control','placeholder':'https://www.example.com'}))
    url_extract_data_back=forms.URLField(widget=forms.URLInput(attrs={'class':'form-control','placeholder':'https://www.example.com'}))