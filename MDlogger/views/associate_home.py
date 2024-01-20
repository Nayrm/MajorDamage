from django.shortcuts import render
from datetime import datetime
from ..models import SavedRepair, Projects

def associate_home(request):
    current_date = datetime.now().date()
    repairs = SavedRepair.objects.filter(user=request.user, date=current_date).select_related('user').order_by('-date', '-time')
    pieces_repaired_today = repairs.count()
    projects = Projects.objects.filter(date=current_date, assignedto = request.user, status="Incomplete").order_by('-date')
    return render(request, 'MDlogger/associate_home.html', {'repairs': repairs,'pieces_repaired_today': pieces_repaired_today , 'projects': projects})