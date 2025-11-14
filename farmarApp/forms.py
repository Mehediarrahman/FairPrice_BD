from django import forms
from farmarApp.models import*


class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = '__all__'


class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = '__all__'


class FarmRecordForm(forms.ModelForm):
    class Meta:
        model = FarmRecord
        fields = '__all__'


class CropExpenseForm(forms.ModelForm):
    class Meta:
        model = CropExpense
        fields = '__all__'


class FieldAgentForm(forms.ModelForm):
    class Meta:
        model = FieldAgent
        fields = '__all__'


class FieldAgentAssignmentForm(forms.ModelForm):
    class Meta:
        model = FieldAgentAssignment
        fields = '__all__'
