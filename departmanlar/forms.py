from django import forms
from .models import DataRecord, ManagerBonus

class DataRecordForm(forms.ModelForm):
    class Meta:
        model = DataRecord
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'data_type': forms.Select(attrs={'class': 'form-control'}),
            'manager_name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_value(self):
        value = self.cleaned_data['value']
        value = str(value).replace('%', '').replace(',', '.')
        try:
            value_float = float(value)
        except (ValueError, TypeError):
            raise forms.ValidationError("Veri sayısal olmalıdır (örn: 11.29 veya %11.29).")
        return value_float

class ManagerBonusForm(forms.ModelForm):
    MONTH_CHOICES = [
        ('1', 'Ocak'),
        ('2', 'Şubat'),
        ('3', 'Mart'),
        ('4', 'Nisan'),
        ('5', 'Mayıs'),
        ('6', 'Haziran'),
        ('7', 'Temmuz'),
        ('8', 'Ağustos'),
        ('9', 'Eylül'),
        ('10', 'Ekim'),
        ('11', 'Kasım'),
        ('12', 'Aralık'),
    ]
    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        label="Ay",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ManagerBonus
        fields = ['department', 'manager_name', 'info_title', 'value', 'month', 'year']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'manager_name': forms.TextInput(attrs={'class': 'form-control'}),
            'info_title': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': 2000, 'max': 2100}),
        }

    def clean_value(self):
        value = self.cleaned_data['value']
        value = str(value).replace('%', '').replace(',', '.')
        try:
            value_float = float(value)
        except (ValueError, TypeError):
            raise forms.ValidationError("Veri sayısal olmalıdır (örn: 11.29 veya %11.29).")
        return value_float