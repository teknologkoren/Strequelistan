from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput, DateTimeInput, ModelForm
from datetime import datetime, timedelta

from .models import Quote, RegisterRequest, Suggestion


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'inputUsername', 'placeholder': 'username'})

    )

    password = forms.CharField(
        label="Password",
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'inputPassword', 'placeholder': 'password'})
    )


class QuoteForm(forms.Form):
    text = forms.CharField(
        label="text",
        required=True,
        max_length=4098,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'inputUsername', 'aria-describedby': 'basic-addon1'})

    )
    name = forms.CharField(
        label="name",

        required=True,
        max_length=250,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'inputUsername', 'aria-describedby': 'basic-addon1'})
    )

    def clean(self):
        form_data = self.cleaned_data
        try:
            if Quote.objects.filter(text=form_data['text'], who=form_data['name']).exists():
                raise ValidationError("Quote already exists")

        except:
            raise ValidationError("Not enough arguments")
        return form_data

class BulkTransactionForm(forms.Form):

    amount=forms.DecimalField(
        required=True,
        max_value=20000,
        max_digits=6,
        label="blargh",
        initial=0
    )
    user_id = forms.IntegerField(
        required=True,
        widget = forms.HiddenInput()
    )
    message = forms.CharField(
        required=True,
        initial="Admin transaction"
    )

class ReturnTransactionForm(forms.Form):
    transaction_id = forms.DecimalField(
        required=True,
    )

class TransactionDateForm(forms.Form):
    start_date = forms.DateField(initial=datetime.now()-timedelta(days=60))
    end_date = forms.DateField(initial=datetime.now())

    class Meta:
        fields = '__all__'
        widgets = {
            'start_date': DateTimeInput(),
            'end_date': DateTimeInput(),
        }

class heddaHopperForm(forms.Form):
    where = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'}
        ),
        required=False,
    )

    when = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'},
        ),
        required=False,
    )

    what = forms.CharField(
        max_length=4000,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'}
        ),
        required=True,
    )

class RegisterRequestForm(forms.Form):
    first_name = forms.CharField(

        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),
    )

    last_name = forms.CharField(
        max_length = 50,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),

    )

    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),
    )

    message = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control'}
        ),
    )

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['name', 'description', 'price', 'link']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'}),
            'link': forms.TextInput(attrs={'class': 'form-control', 'aria-describedby': 'basic-addon1'}),
        }
