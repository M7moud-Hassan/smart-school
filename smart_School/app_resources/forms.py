from django import forms

from .models import Cameras, Persons


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
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 5})


class PersonsForm(forms.ModelForm):
    class Meta:
        model = Persons
        fields = ['name', 'gender', 'date_of_birth', 'image', 'status']

        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'dropify-face form-control',"data-default-file":"",'required': True,}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#reservationdate',
                'required': True,

            }),

        }
        labels = {
            'image': 'image person'
        }

    # Customizing the gender field widget to use radio buttons
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, initial='Male')
    status = forms.ChoiceField(choices=[('whitelist', 'whitelist'), ('blacklist', 'blacklist')])

    def __init__(self, *args, **kwargs):
        super(PersonsForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-control'
