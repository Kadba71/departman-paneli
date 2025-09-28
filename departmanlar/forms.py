from django import forms
from .models import DataRecord, ManagerBonus, Contact, BulkMessage

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
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'department', 'notes', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kişinin adını giriniz'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+90 5XX XXX XX XX'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Departman (opsiyonel)'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notlar (opsiyonel)'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        # Telefon numarasının formatını kontrol et
        phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if not phone.startswith('+'):
            if phone.startswith('0'):
                phone = '+90' + phone[1:]
            elif not phone.startswith('90'):
                phone = '+90' + phone
            else:
                phone = '+' + phone
        return phone

class BulkMessageForm(forms.ModelForm):
    recipients = forms.ModelMultipleChoiceField(
        queryset=Contact.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label="Alıcılar",
        help_text="Mesaj gönderilecek kişileri seçin"
    )

    class Meta:
        model = BulkMessage
        fields = ['message_content', 'recipients']
        widgets = {
            'message_content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Gönderilecek mesajı buraya yazın...',
                'maxlength': 1000
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message_content'].label = "Mesaj İçeriği"