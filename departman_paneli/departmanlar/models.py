from django.db import models

class Departman(models.Model):
    isim = models.CharField(max_length=255)

    def __str__(self):
        return self.isim

class Veri(models.Model):
    departman = models.ForeignKey(Departman, on_delete=models.CASCADE)
    baslik = models.CharField(max_length=255)
    deger = models.CharField(max_length=255)
    tarih = models.DateField()  # <-- Geçmiş ve istenen tarih için bu alanı ekle

    def __str__(self):
        return f"{self.departman} - {self.baslik} ({self.tarih})"