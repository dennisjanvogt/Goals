from django import forms
from .models import Goal
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['definition', 'description', 'ziel_wert', 'fortschritt', 'einheit', 'start', 'end', 'kategorie']
        widgets = {
            'definition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ziel definieren'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Beschreibung des Ziels'}),
            'ziel_wert': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Zielwert'}),
            'fortschritt': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Aktueller Fortschritt'}),
            'einheit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'z.B. km, Bücher, €'}),
            'start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'kategorie': forms.Select(attrs={'class': 'form-control'})
        }
        
    def clean_fortschritt(self):
        fortschritt = self.cleaned_data.get('fortschritt')
        ziel_wert = self.cleaned_data.get('ziel_wert')
        
        if fortschritt and ziel_wert and fortschritt > ziel_wert:
            raise forms.ValidationError("Der Fortschritt kann nicht größer als der Zielwert sein.")
        
        return fortschritt
    
    def clean_end(self):
        start = self.cleaned_data.get('start')
        end = self.cleaned_data.get('end')
        
        if start and end and end < start:
            raise forms.ValidationError("Das Enddatum kann nicht vor dem Startdatum liegen.")
        
        return end
    


class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form with better error messages
    """
    error_messages = {
        'invalid_login': _(
            "Bitte gib einen gültigen Benutzernamen und ein Passwort ein. "
            "Die Eingaben sind möglicherweise falsch."
        ),
        'inactive': _("Dieses Konto ist inaktiv."),
    }
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Benutzername'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Passwort'}),
    )