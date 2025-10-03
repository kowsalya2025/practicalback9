from django import forms
from .models import Job, Application, Interview

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title','description','location']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter','resume']

class InterviewForm(forms.ModelForm):
    scheduled_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))
    class Meta:
        model = Interview
        fields = ['scheduled_at','location','notes']
