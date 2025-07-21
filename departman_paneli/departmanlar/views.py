from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Departman, Veri

@login_required
def dashboard(request):
    ay = request.GET.get("ay")
    hafta = request.GET.get("hafta")

    def hafta_belirle(tarih):
        gun = tarih.day
        if 1 <= gun <= 7:
            return "1"
        elif 8 <= gun <= 14:
            return "2"
        elif 15 <= gun <= 21:
            return "3"
        elif 22 <= gun <= 28:
            return "4"
        else:
            return "tumu"

    def veri_filtrele(departman):
        qs = Veri.objects.filter(departman=departman)
        if ay:
            qs = qs.filter(tarih__month=int(ay))
        if hafta and hafta != "tumu":
            qs = [v for v in qs if hafta_belirle(v.tarih) == hafta]
        return qs

    # Dış ekipler
    dis_ekip_1 = Departman.objects.filter(isim="Dış Data-1 ( Murat )").first()
    dis_ekip_2 = Departman.objects.filter(isim="Dış Data-2 ( Mertcan )").first()
    dis_ekip_1_veriler = veri_filtrele(dis_ekip_1) if dis_ekip_1 else []
    dis_ekip_2_veriler = veri_filtrele(dis_ekip_2) if dis_ekip_2 else []

    # İç ekipler
    ic_departman_isimleri = [
        "Karşılama Ekibi",
        "Dönüşüm Ekibi",
        "Yatırımlı Pasif Ekibi",
        "Retation Ekibi"
    ]
    ic_departmanlar = Departman.objects.filter(isim__in=ic_departman_isimleri)
    ic_veriler = []
    for dep in ic_departmanlar:
        veriler = veri_filtrele(dep)
        ic_veriler.append({"departman": dep, "veriler": veriler})

    aylar = range(1, 13)
    context = {
        "dis_ekip_1": dis_ekip_1,
        "dis_ekip_2": dis_ekip_2,
        "dis_ekip_1_veriler": dis_ekip_1_veriler,
        "dis_ekip_2_veriler": dis_ekip_2_veriler,
        "ic_veriler": ic_veriler,
        "aylar": aylar,
        "request": request,
    }
    return render(request, "departmanlar/dashboard.html", context)