from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "body"]
        labels = {"body": "Note"}


class RegistrationForm(UserCreationForm):
    def clean_password1(self):
        password = self.cleaned_data["password1"]
        limit = 48
        # Fix 4: give people room to use a longer passphrase.
        # limit = 128
        if len(password) > limit:
            raise forms.ValidationError(f"This form only accepts passphrases up to {limit} characters long.")
        return password
