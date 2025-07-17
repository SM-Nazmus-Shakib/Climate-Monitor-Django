from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import DamageReport
from .forms import DamageReportForm, DamageReportVerificationForm
from farms.models import Farm

@login_required
def report_list(request):
    if request.user.has_perm('damage_report.can_verify_reports'):
        reports = DamageReport.objects.all().order_by('-date_reported')
    else:
        reports = DamageReport.objects.filter(reported_by=request.user).order_by('-date_reported')
    
    return render(request, 'damage_report/report_list.html', {'reports': reports})

@login_required
def report_detail(request, pk):
    report = get_object_or_404(DamageReport, pk=pk)
    
    if not request.user.has_perm('damage_report.can_verify_reports') and report.reported_by != request.user:
        messages.error(request, "You don't have permission to view this report.")
        return redirect('damage_report:list')
    
    return render(request, 'damage_report/report_detail.html', {'report': report})

@login_required
def create_report(request, farm_id=None):
    farms = Farm.objects.filter(owner=request.user)
    
    if request.method == 'POST':
        form = DamageReportForm(request.user, request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reported_by = request.user
            report.save()
            messages.success(request, 'Damage report submitted successfully!')
            return redirect('damage_report:detail', pk=report.pk)
    else:
        initial = {'farm': farm_id} if farm_id else {}
        form = DamageReportForm(request.user, initial=initial)
    
    return render(request, 'damage_report/create_report.html', {
        'form': form,
        'farms': farms
    })

@login_required
@permission_required('damage_report.can_verify_reports', raise_exception=True)
def verify_report(request, pk):
    report = get_object_or_404(DamageReport, pk=pk)
    
    if request.method == 'POST':
        form = DamageReportVerificationForm(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.verified_by = request.user
            report.is_verified = True
            report.save()
            messages.success(request, 'Report verified successfully!')
            return redirect('damage_report:detail', pk=report.pk)
    else:
        form = DamageReportVerificationForm(instance=report)
    
    return render(request, 'damage_report/verify_report.html', {
        'form': form,
        'report': report
    })