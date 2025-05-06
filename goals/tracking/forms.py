# tracking/forms.py
from django import forms
from .models import Goal
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import YearlyGoal

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['definition', 'description', 'ziel_wert', 'fortschritt', 'einheit', 'start', 'end', 'kategorie', 'parent', 'auto_calculate']
        widgets = {
            'definition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ziel definieren'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Beschreibung des Ziels'}),
            'ziel_wert': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Zielwert'}),
            'fortschritt': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Aktueller Fortschritt'}),
            'einheit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'z.B. km, Bücher, €'}),
            # Ensure proper date formatting for HTML5 date inputs
            'start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'kategorie': forms.Select(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'auto_calculate': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Set default start date for new goals (when instance is None)
        if not self.instance.pk and not self.initial.get('start'):
            self.initial['start'] = timezone.now().date()
        
        if user:
            # Filter nur Hauptziele dieses Benutzers als mögliche Elternziele
            parent_goals = Goal.objects.filter(user=user, parent__isnull=True)
            self.fields['parent'].queryset = parent_goals
            self.fields['parent'].label = "Übergeordnetes Ziel (optional)"
            self.fields['parent'].required = False
            
            # Auto-Calculate Field Erklärung
            self.fields['auto_calculate'].label = "Fortschritt automatisch berechnen"
            
        # Fortschritt-Feld als optional markieren für automatisch berechnete Ziele
        self.fields['fortschritt'].required = False
        
    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get('parent')
        auto_calculate = cleaned_data.get('auto_calculate')
        fortschritt = cleaned_data.get('fortschritt')
        
        # Wenn kein Elternziel ausgewählt ist und auto_calculate aktiviert ist
        if not parent and auto_calculate:
            # Hier könnten wir eine Warnung anzeigen, dass auto_calculate
            # nur bei Elternzielen sinnvoll ist, aber wir erlauben es trotzdem
            pass
            
        # Wenn auto_calculate aktiviert ist und kein Fortschritt angegeben wurde,
        # setze Fortschritt auf 0 als Startwert
        if auto_calculate and fortschritt is None:
            cleaned_data['fortschritt'] = 0
            
        return cleaned_data
        
    def clean_fortschritt(self):
        fortschritt = self.cleaned_data.get('fortschritt')
        ziel_wert = self.cleaned_data.get('ziel_wert')
        auto_calculate = self.cleaned_data.get('auto_calculate')
        
        # Wenn auto_calculate aktiviert ist, kann fortschritt None sein
        if auto_calculate and fortschritt is None:
            return 0
            
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



class YearlyGoalForm(forms.ModelForm):
    class Meta:
        model = YearlyGoal
        fields = ['title', 'description', 'year', 'start_value', 'target_value', 'unit',
                 'january', 'february', 'march', 'april', 'may', 'june',
                 'july', 'august', 'september', 'october', 'november', 'december']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titel des Jahresziels'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Beschreibung des Jahresziels'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
            'start_value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Anfangswert'}),
            'target_value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Zielwert'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Einheit (z.B. Abonnenten, kg, €)'}),
            'january': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Januar'}),
            'february': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Februar'}),
            'march': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'März'}),
            'april': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'April'}),
            'may': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Mai'}),
            'june': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Juni'}),
            'july': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Juli'}),
            'august': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'August'}),
            'september': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'September'}),
            'october': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Oktober'}),
            'november': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'November'}),
            'december': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Dezember'}),
        }