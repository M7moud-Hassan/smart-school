from django import forms

from .models import Cameras


class CamerasForm(forms.ModelForm):
    class Meta:
        model = Cameras
        fields = ['name', 'camera_type', 'status', 'description', 'connection_string']
    camera_type = forms.ChoiceField(choices=[('indoor', 'Indoor'), ('outdoor', 'Outdoor')])
    status = forms.ChoiceField(choices=[('enable', 'Enable'), ('disable', 'Disable')])

    def __init__(self, *args, **kwargs):
        super(CamerasForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Name of Camera'
        self.fields['connection_string'].widget.attrs['placeholder'] = 'connection string'
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control','rows': 5})
