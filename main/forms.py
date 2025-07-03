from django import forms
#from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import  Note

"""class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)"""

"""class NoteUploadForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description', 'file_path']"""

class NoteUploadForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description', 'file', 'subject']  # ✅ Correct fields