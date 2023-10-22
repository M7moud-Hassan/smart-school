from django import forms

from .models import *
from django_select2.forms import Select2MultipleWidget


class CamerasForm(forms.ModelForm):
    class Meta:
        model = Cameras
        fields = ['name', 'camera_type', 'status',
                  'description', 'connection_string']

    camera_type = forms.ChoiceField(
        choices=[('indoor', 'Indoor'), ('outdoor', 'Outdoor')])
    status = forms.ChoiceField(
        choices=[('enable', 'Enable'), ('disable', 'Disable')])

    def __init__(self, *args, **kwargs):
        super(CamerasForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Name of Camera'
        self.fields['connection_string'].widget.attrs['placeholder'] = 'connection string'
        self.fields['description'].widget = forms.Textarea(
            attrs={'class': 'form-control', 'rows': 5})


class PersonsForm(forms.ModelForm):
    class Meta:
        model = Persons
        fields = ['name', 'gender', 'date_of_birth', 'image', 'status', 'allowed_cameras', 'front_national_img',
                  'back_national_img',
                  'id_national', 'address', 'job_title','type_register']
        widgets = {
            'image': forms.ClearableFileInput(
                attrs={'class': 'dropify-face form-control', "data-default-file": "", 'required': True, }),
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'date_of_birth': forms.TextInput(attrs={
                'class': 'form-control',
                'id':'date',
                'required': True,
            }),
            'front_national_img': forms.ClearableFileInput(
                attrs={'class': 'dropify-front form-control', "data-default-file": "", 'required': True}),
            'back_national_img': forms.ClearableFileInput(
                attrs={'class': 'dropify-back form-control', "data-default-file": "", 'required': True}),
            'id_national': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }
        labels = {
            'image': 'الصور الشخصية',
            'front_national_img': 'صورة البطاقة الامامية',
            'back_national_img': 'صورة البطاقة الخلفية',
            'job_title': 'الاسم الوظيفة'
        }
        allowed_cameras = forms.ModelMultipleChoiceField(
            queryset=Cameras.objects.all(),
            widget=Select2MultipleWidget(attrs={'style': 'width: 100%;',
                                                'class': "select2", 'multiple': "multiple",
                                                'data-placeholder': "Select a State",

                                                }),
            required=True,

        )

    # Customizing the gender field widget to use radio buttons
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    TYPE_CHOICES = [
             ('Visitor', 'Visitor'),
            ('Employee', 'Employee'),
]
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, widget=forms.RadioSelect, initial='Male')
    type_register = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='Employee'
    )
    status = forms.ChoiceField(choices=[(
        'whitelist', 'whitelist'), ('blacklist', 'blacklist'), ('unknown', 'unknown')])

    def __init__(self, *args, **kwargs):
        super(PersonsForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-control'


class InformationsForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = ['department', 'type', 'reason', 'other', 'visior_type']
    department = forms.ModelChoiceField(
        label='department',
        queryset=Department.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control select2', 'placeholder': 'Branch'}),
        required=True
    )
    type = forms.ModelChoiceField(
        label='type',
        queryset=Type.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control select2', 'placeholder': 'Branch'}),
        required=True
    )
    reason = forms.ModelChoiceField(
        label='reason',
        queryset=Reason.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control select2', 'placeholder': 'Branch'}),
        required=True
    )
    other = forms.ModelChoiceField(
        label='other',
        queryset=Other.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control select2', 'placeholder': 'Branch'}),
        required=True
    )
    visior_type = forms.ModelChoiceField(
        label='visior type',
        queryset=VisiTortype.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control select2', 'placeholder': 'Branch'}),
        required=True
    )
