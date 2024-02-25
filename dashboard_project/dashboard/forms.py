# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Feedback, ActivityLog

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class FeedbackForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)
    
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'date', 'message']
        
class ActivityLogForm(forms.ModelForm):
    action = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = ActivityLog
        fields = ['action']

    def save_activity_log(self, user):
        action = self.cleaned_data['action']
        ActivityLog.objects.create(user=user, action=action)