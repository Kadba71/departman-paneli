from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import DataRecord, ManagerBonus
from .forms import DataRecordForm, ManagerBonusForm
from django.http import HttpResponse
from openpyxl import Workbook

BONUS_DEPARTMENTS = [
    ('Dış Ekip-1 (Murat)', 'Dış Ekip-1 (Murat)'),
    ('Dış Ekip-2 (Mertcan)', 'Dış Ekip-2 (Mertcan)'),
    ('Karşılama Ekibi (Ece)', 'Karşılama Ekibi (Ece)'),
    ('Dönüşüm Ekibi (Alper)', 'Dönüşüm Ekibi (Alper)'),
    ('Yatırımlı Pasif Ekibi (Asuman)', 'Yatırımlı Pasif Ekibi (Asuman)'),
    ('Retation Ekibi (Asuman)', 'Retation Ekibi (Asuman)'),
]

def dashboard(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')
    search = request.GET.get('search')

    ekipler = [
        'Karşılama Ekibi (Ece)',
        'Dönüşüm Ekibi (Alper)',
        'Yatırımlı Pasif Ekibi (Asuman)',
        'Retation Ekibi (Asuman)',
    ]

    records = DataRecord.objects.all()
    if year:
        records = records.filter(date__year=year)
    if month:
        records = records.filter(date__month=month)
    if day:
        records = records.filter(date__day=day)
    if search:
        records = records.filter(title__icontains=search)

    bonuses = ManagerBonus.objects.all().order_by('-year', '-month', '-id')

    years = DataRecord.objects.values_list('date__year', flat=True).distinct().order_by('date__year')
    months = range(1, 13)
    days = range(1, 32)

    data_form = DataRecordForm()
    bonus_form = ManagerBonusForm()

    if request.method == 'POST':
        if 'veri_ekle' in request.POST:
            data_form = DataRecordForm(request.POST)
            if data_form.is_valid():
                data_form.save()
                messages.success(request, "Veri başarıyla eklendi.")
                return redirect('dashboard')
            else:
                messages.error(request, "Formda hata var.")
        elif 'prim_ekle' in request.POST:
            bonus_form = ManagerBonusForm(request.POST)
            if bonus_form.is_valid():
                bonus_form.save()
                messages.success(request, "Prim başarıyla eklendi.")
                return redirect('dashboard')
            else:
                messages.error(request, "Prim formunda hata var.")

    context = {
        'form': data_form,
        'records': records,
        'years': years,
        'months': months,
        'days': days,
        'search': search,
        'ekipler': ekipler,
        'bonuses': bonuses,
        'bonus_form': bonus_form,
        'messages': messages.get_messages(request),
        'bonus_departments': BONUS_DEPARTMENTS,
    }
    return render(request, 'departmanlar/dashboard.html', context)

def delete_data(request, pk):
    record = get_object_or_404(DataRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, "Veri silindi.")
    return redirect('dashboard')

def edit_data(request, pk):
    record = get_object_or_404(DataRecord, pk=pk)
    if request.method == 'POST':
        form = DataRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Veri güncellendi.")
            return redirect('dashboard')
        else:
            messages.error(request, "Formda hata var.")
    else:
        form = DataRecordForm(instance=record)
    return render(request, 'departmanlar/edit_data.html', {'form': form, 'record': record})

def delete_bonus(request, pk):
    bonus = get_object_or_404(ManagerBonus, pk=pk)
    if request.method == 'POST':
        bonus.delete()
        messages.success(request, "Prim silindi.")
    return redirect('dashboard')

def edit_bonus(request, pk):
    bonus = get_object_or_404(ManagerBonus, pk=pk)
    if request.method == 'POST':
        form = ManagerBonusForm(request.POST, instance=bonus)
        if form.is_valid():
            form.save()
            messages.success(request, "Prim güncellendi.")
            return redirect('dashboard')
        else:
            messages.error(request, "Formda hata var.")
    else:
        form = ManagerBonusForm(instance=bonus)
    return render(request, 'departmanlar/edit_bonus.html', {'form': form, 'bonus': bonus})

def export_data(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    records = DataRecord.objects.all()
    if start_date and end_date:
        records = records.filter(date__range=[start_date, end_date])
    bonuses = ManagerBonus.objects.all()

    wb = Workbook()
    ws1 = wb.active
    ws1.title = "Data Records"
    ws1.append(['Departman', 'Yönetici', 'Tür', 'Başlık', 'Veri', 'Tarih'])
    for record in records:
        ws1.append([
            record.department,
            record.manager_name,
            record.data_type,
            record.title,
            record.value,
            record.date.strftime('%d.%m.%Y') if record.date else ''
        ])

    ws2 = wb.create_sheet(title="Yönetici Primleri")
    ws2.append(['Yönetici', 'Başlık', 'Veri', 'Ay', 'Yıl', 'Departman'])
    for bonus in bonuses:
        ws2.append([
            bonus.manager_name,
            bonus.info_title,
            bonus.value,
            bonus.month,
            bonus.year,
            bonus.department
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="panel_verileri.xlsx"'
    wb.save(response)
    return response