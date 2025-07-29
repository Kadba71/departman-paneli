from django.db import models

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