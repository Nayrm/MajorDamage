from django import forms
from django.contrib.auth.models import User
from .models import Projects

class AddRepairForm(forms.Form):
    REPAIR_CHOICES = [
    ('Assembled', 'Assembled'),
    ('Back Panel', 'Back Panel'),
    ('Broken Door', 'Broken Door'),
    ('Broken Frame', 'Broken Frame'),
    ('Broken Glass', 'Broken Glass'),
    ('Broken Glides', 'Broken Glides'),
    ('Broken Hinges', 'Broken Hinges'),
    ('Broken Top', 'Broken Top'),
    ('Disassembled', 'Disassembled'),
    ('Installed New Part', 'Installed New Part'),
    ('Missing Hardware', 'Missing Hardware'),
    ('Missing Slats/supports', 'Missing Slats/Supports'),
            # Add more choices as needed
    ]

    repair = forms.ChoiceField(choices=REPAIR_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['assignedto', 'due', 'department', 'project', 'description']

       

    def __init__(self, *args, **kwargs):
        super(ProjectsForm, self).__init__(*args, **kwargs)
        # Update assignedto field to use a ModelChoiceField with queryset of User objects
        self.fields['assignedto'] = forms.ModelChoiceField(
            queryset=User.objects.all(),
            required=False,  # You can set this to True if you want it to be a required field
            widget=forms.Select(attrs={'class': 'form-control'}),
        )