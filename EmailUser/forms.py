from django import forms

class UpdateUserForm(forms.Form):
    nickname = forms.CharField(
        label="Nickname",
        required=False,
        max_length=50,
    )

    avatar = forms.ImageField(
        required=False,
    )

    phone_number = forms.CharField(
        max_length=20,
        required=False
    )

    email = forms.EmailField(
        required=False
    )

    password = forms.CharField(
        required=False
    )

    weight = forms.DecimalField(
        decimal_places=20,
        label="Hur mycket väger du (i kg)? (används för att beräkna alkoholhalt i blodet bättre)",
        required = False
    )

    CHOICES = [
               ('none', 'Vill ej uppge'),
                ('y', 'Jag har en y kromosom'),
               ('not_y', 'Jag har inte en y kromosom')]

    y_chromosome = forms.ChoiceField(
        required=False,
        choices=CHOICES,
        label="Har du en Y kromosom? (används för att beräkna alkoholhalt i blodet bättre)"
    )

    user_id = forms.IntegerField()

class UpdateUserImageForm(forms.Form):
    avatar = forms.ImageField(
        required=True
    )
    id = forms.IntegerField(
        required=True,
        widget = forms.HiddenInput()
    )
