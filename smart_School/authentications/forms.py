from django import forms

from authentications.models import Branch


class LoginForm(forms.Form):
    email = forms.EmailField(label='email',required=True,widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}))
    password = forms.CharField(label='password',required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))
    branches = forms.ModelChoiceField(
        label='Branch',
        queryset=Branch.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'placeholder': 'Branch'}),
        required=True
    )


