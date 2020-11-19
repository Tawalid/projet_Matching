from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(EmployeeForm,self).__init__(*args, **kwargs)
        self.fields['sexe'].empty_label = "Select"
        self.fields['portable'].required = False
        self.fields['divers'].required = False
        self.fields['sexe'].required = False
        self.fields['experiences1'].required = False
        self.fields['experiences2'].required = False
        self.fields['experiences3'].required = False