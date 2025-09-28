from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import DataRecord, ManagerBonus, Contact, BulkMessage
from .forms import DataRecordForm, ManagerBonusForm, ContactForm, BulkMessageForm
from django.http import HttpResponse, JsonResponse
from openpyxl import Workbook
from django.contrib.auth.decorators import login_required
import threading
import time
from concurrent.futures import ThreadPoolExecutor

BONUS_DEPARTMENTS = [
    ('Dış Ekip-1 (Murat)', 'Dış Ekip-1 (Murat)'),
    ('Dış Ekip-2 (Mertcan)', 'Dış Ekip-2 (Mertcan)'),
    ('Karşılama Ekibi (Ece)', 'Karşılama Ekibi (Ece)'),
    ('Dönüşüm Ekibi (Alper)', 'Dönüşüm Ekibi (Alper)'),
    ('Yatırımlı Pasif Ekibi (Asuman)', 'Yatırımlı Pasif Ekibi (Asuman)'),
    ('Retation Ekibi (Asuman)', 'Retation Ekibi (Asuman)'),
]

@login_required(login_url='/login/')
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

# Mock messaging function - simulate sending messages
def simulate_send_message(phone_number, message_content):
    """Simulate sending a message to a phone number"""
    # In a real implementation, this would integrate with a messaging service like Twilio
    time.sleep(0.5)  # Simulate network delay
    # For now, we'll simulate success for all messages
    import random
    success = random.choice([True, True, True, False])  # 75% success rate
    return success

@login_required(login_url='/login/')
def bulk_message_panel(request):
    """View for bulk messaging functionality"""
    contacts = Contact.objects.filter(is_active=True).order_by('name')
    contact_form = ContactForm()
    bulk_message_form = BulkMessageForm()
    recent_messages = BulkMessage.objects.filter(sender=request.user).order_by('-sent_at')[:10]
    
    # Handle POST requests
    if request.method == 'POST':
        if 'add_contact' in request.POST:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact_form.save()
                messages.success(request, "Kişi başarıyla eklendi.")
                return redirect('bulk_message_panel')
            else:
                messages.error(request, "Kişi eklenirken hata oluştu.")
                
        elif 'send_bulk_message' in request.POST:
            bulk_message_form = BulkMessageForm(request.POST)
            if bulk_message_form.is_valid():
                # Create the bulk message record
                bulk_message = bulk_message_form.save(commit=False)
                bulk_message.sender = request.user
                bulk_message.total_recipients = bulk_message_form.cleaned_data['recipients'].count()
                bulk_message.save()
                bulk_message_form.save_m2m()  # Save many-to-many relationships
                
                # Get recipients and message content
                recipients = bulk_message_form.cleaned_data['recipients']
                message_content = bulk_message_form.cleaned_data['message_content']
                
                # Start async message sending
                send_bulk_messages_async(bulk_message.id, recipients, message_content)
                
                messages.success(request, f"Mesaj {recipients.count()} kişiye gönderiliyor...")
                return redirect('bulk_message_panel')
            else:
                messages.error(request, "Mesaj gönderilirken hata oluştu.")
    
    context = {
        'contacts': contacts,
        'contact_form': contact_form,
        'bulk_message_form': bulk_message_form,
        'recent_messages': recent_messages,
    }
    return render(request, 'departmanlar/bulk_message_panel.html', context)

def send_bulk_messages_async(bulk_message_id, recipients, message_content):
    """Send messages asynchronously using threading"""
    def send_messages():
        try:
            bulk_message = BulkMessage.objects.get(id=bulk_message_id)
            success_count = 0
            failed_count = 0
            
            # Use ThreadPoolExecutor for concurrent sending
            with ThreadPoolExecutor(max_workers=10) as executor:
                # Create futures for all message sending tasks
                futures = []
                for contact in recipients:
                    future = executor.submit(simulate_send_message, contact.phone_number, message_content)
                    futures.append((contact, future))
                
                # Process results
                for contact, future in futures:
                    try:
                        success = future.result(timeout=30)  # 30 second timeout per message
                        if success:
                            success_count += 1
                        else:
                            failed_count += 1
                    except Exception as e:
                        failed_count += 1
                        print(f"Error sending to {contact.phone_number}: {e}")
            
            # Update the bulk message record
            bulk_message.success_count = success_count
            bulk_message.failed_count = failed_count
            bulk_message.save()
            
        except Exception as e:
            print(f"Error in bulk message sending: {e}")
    
    # Start the thread
    thread = threading.Thread(target=send_messages)
    thread.daemon = True
    thread.start()

@login_required(login_url='/login/')
def delete_contact(request, pk):
    """Delete a contact"""
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, "Kişi silindi.")
    return redirect('bulk_message_panel')

@login_required(login_url='/login/')
def edit_contact(request, pk):
    """Edit a contact"""
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, "Kişi güncellendi.")
            return redirect('bulk_message_panel')
        else:
            messages.error(request, "Formda hata var.")
    else:
        form = ContactForm(instance=contact)
    return render(request, 'departmanlar/edit_contact.html', {'form': form, 'contact': contact})

@login_required(login_url='/login/')
def message_status(request, message_id):
    """Get the status of a bulk message"""
    try:
        bulk_message = BulkMessage.objects.get(id=message_id, sender=request.user)
        return JsonResponse({
            'total': bulk_message.total_recipients,
            'success': bulk_message.success_count,
            'failed': bulk_message.failed_count,
            'completed': bulk_message.success_count + bulk_message.failed_count == bulk_message.total_recipients
        })
    except BulkMessage.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)