from django import forms

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
