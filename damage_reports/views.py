from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DamageReport, DamagePhoto
from .forms import DamageReportForm, DamagePhotoForm

@login_required
def report_list(request):
    reports = DamageReport.objects.filter(reporter=request.user).order_by('-created_at')
    context = {'reports': reports}
    return render(request, 'damage_reports/report_list.html', context)

@login_required
def report_detail(request, report_id):
    report = get_object_or_404(DamageReport, id=report_id, reporter=request.user)
    photos = DamagePhoto.objects.filter(damage_report=report)
    
    context = {
        'report': report,
        'photos': photos,
    }
    return render(request, 'damage_reports/report_detail.html', context)

@login_required
def report_create(request):
    if request.method == 'POST':
        form = DamageReportForm(request.user, request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.save()
            messages.success(request, 'Damage report submitted successfully!')
            return redirect('damage_reports:report_detail', report_id=report.id)
    else:
        form = DamageReportForm(request.user)
    
    context = {'form': form, 'title': 'Submit Damage Report'}
    return render(request, 'damage_reports/report_form.html', context)

@login_required
def report_edit(request, report_id):
    report = get_object_or_404(DamageReport, id=report_id, reporter=request.user)
    
    if request.method == 'POST':
        form = DamageReportForm(request.user, request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Damage report updated successfully!')
            return redirect('damage_reports:report_detail', report_id=report.id)
    else:
        form = DamageReportForm(request.user, instance=report)
    
    context = {'form': form, 'title': 'Edit Damage Report', 'report': report}
    return render(request, 'damage_reports/report_form.html', context)