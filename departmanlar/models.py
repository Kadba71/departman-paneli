from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="İsim")
    phone_number = models.CharField(max_length=20, verbose_name="Telefon Numarası")
    department = models.CharField(max_length=100, blank=True, verbose_name="Departman")
    notes = models.TextField(blank=True, verbose_name="Notlar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")

    def __str__(self):
        return f"{self.name} - {self.phone_number}"

    class Meta:
        verbose_name = "Kişi"
        verbose_name_plural = "Kişiler"
        ordering = ['name']

class BulkMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Gönderen")
    message_content = models.TextField(verbose_name="Mesaj İçeriği")
    recipients = models.ManyToManyField(Contact, verbose_name="Alıcılar")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Gönderilme Tarihi")
    total_recipients = models.IntegerField(default=0, verbose_name="Toplam Alıcı")
    success_count = models.IntegerField(default=0, verbose_name="Başarılı Gönderim")
    failed_count = models.IntegerField(default=0, verbose_name="Başarısız Gönderim")

    def __str__(self):
        return f"Toplu Mesaj - {self.sent_at.strftime('%d.%m.%Y %H:%M')}"

    class Meta:
        verbose_name = "Toplu Mesaj"
        verbose_name_plural = "Toplu Mesajlar"
        ordering = ['-sent_at']

class DataRecord(models.Model):
    DEPARTMENT_CHOICES = [
        ('Dış Ekip-1 (Murat)', 'Dış Ekip-1 (Murat)'),
        ('Dış Ekip-2 (Mertcan)', 'Dış Ekip-2 (Mertcan)'),
        ('Karşılama Ekibi (Ece)', 'Karşılama Ekibi (Ece)'),
        ('Dönüşüm Ekibi (Alper)', 'Dönüşüm Ekibi (Alper)'),
        ('Yatırımlı Pasif Ekibi (Asuman)', 'Yatırımlı Pasif Ekibi (Asuman)'),
        ('Retation Ekibi (Asuman)', 'Retation Ekibi (Asuman)'),
    ]
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    
    DATA_TYPE_CHOICES = (
        ('dis', 'Dış Data'),
        ('ic', 'İç Data'),
    )
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default="Dış Ekip-1 (Murat)")
    manager_name = models.CharField(max_length=100, default="Bilinmiyor")
    data_type = models.CharField(max_length=10, choices=DATA_TYPE_CHOICES, default="dis")
    title = models.CharField(max_length=100, default="Bilinmiyor")
    value = models.FloatField(default=0)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.department} - {self.title} ({self.date})"

class ManagerBonus(models.Model):
    DEPARTMENT_CHOICES = [
        ('Dış Ekip-1 (Murat)', 'Dış Ekip-1 (Murat)'),
        ('Dış Ekip-2 (Mertcan)', 'Dış Ekip-2 (Mertcan)'),
        ('Karşılama Ekibi (Ece)', 'Karşılama Ekibi (Ece)'),
        ('Dönüşüm Ekibi (Alper)', 'Dönüşüm Ekibi (Alper)'),
        ('Yatırımlı Pasif Ekibi (Asuman)', 'Yatırımlı Pasif Ekibi (Asuman)'),
        ('Retation Ekibi (Asuman)', 'Retation Ekibi (Asuman)'),
    ]
    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        default="Dış Ekip-1 (Murat)"
    )
    manager_name = models.CharField(max_length=100, default="Bilinmiyor")
    info_title = models.CharField(max_length=100, default="Bilinmiyor")
    value = models.FloatField(default=0)
    month = models.IntegerField(default=1)
    year = models.IntegerField(default=2025)

    def __str__(self):
        return f"{self.manager_name} - {self.info_title} ({self.month}.{self.year})"