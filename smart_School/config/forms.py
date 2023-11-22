from django import forms

from app_resources.models import Persons

from .models import Config,Nabatshieh, Reasons,AddDuration

class ConfigForm(forms.ModelForm):
    class Meta:
        model=Config
        fields='__all__'
    time_start_working=forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type':'time'}))
    num_hour_working=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    url_extract_data=forms.URLField(widget=forms.URLInput(attrs={'class':'form-control','placeholder':'https://www.example.com'}))
    url_image=forms.URLField(widget=forms.URLInput(attrs={'class':'form-control','placeholder':'https://www.example.com'}))
    url_extract_data_back=forms.URLField(widget=forms.URLInput(attrs={'class':'form-control','placeholder':'https://www.example.com'}))

class AddSheftForm(forms.ModelForm):
    class Meta:
        model=Nabatshieh
        fields='__all__'
    time_start_working=forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type':'time'}),required=True)
    num_hour_working=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}),required=True)
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
    persions = forms.ModelMultipleChoiceField(
    queryset=Persons.objects.all(),
    widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'assigned-team-members'}),
    required=False
    )
    # def __init__(self, *args, **kwargs):
    #     super(AddSheftForm, self).__init__(*args, **kwargs)

    #     if self.instance and self.instance.id:
    #         nabatshieh_id = self.instance.id
    #         selected_nabatshieh = Nabatshieh.objects.get(pk=nabatshieh_id)
    #         persons_in_nabatshieh = selected_nabatshieh.persions.all()
    #         self.fields['persions'].queryset = persons_in_nabatshieh
    #     else:
    #         persons_not_in_nabatshieh = Persons.objects.exclude(nabatshieh__isnull=False)
    #         self.fields['persions'].queryset = persons_not_in_nabatshieh

class WhenForm(forms.ModelForm):
    WHEN_CHOICES = [
        ('الدخول', 'الدخول'),
        ('الخروج', 'الخروج'),
    ]

    when = forms.ChoiceField(
        choices=WHEN_CHOICES, widget=forms.RadioSelect, initial='entry',required=True
    )
    fromm=forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type':'time'}),required=False)
    too=forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control','type':'time'}),required=False)
    persions = forms.ModelMultipleChoiceField(
    queryset=Persons.objects.all(),
    widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'assigned-team-members'}),
    required=False 
    )
    num_reason=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','type':'number'}))

    class Meta:
        model = Reasons
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AddDurationForm(forms.ModelForm):
    class Meta:
        model = AddDuration
        fields = '__all__'
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
    num_hour_working=forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}),required=True)
    persions = forms.ModelMultipleChoiceField(
    queryset=Persons.objects.all(),
    widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'assigned-team-members'}),
    required=False
    )
    