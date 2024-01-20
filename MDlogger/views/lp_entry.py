from django.shortcuts import render
from django.shortcuts import redirect, render
from datetime import datetime
from ..models import SavedRepair

def lp_entry(request):
    lp = None
    previous_repairs = None

    if request.method == "POST":
        lp = request.POST.get('lp') 
        if SavedRepair.objects.filter(lp=lp, date=datetime.now().date()).exists():

            previous_repairs = SavedRepair.objects.filter(lp=lp, date=datetime.now().date())
        else:
            request.session['lp'] = lp
            return redirect('MDlogger:sku_entry')

    return render(request, 'MDlogger/lp_entry.html', {'lp': lp, 'previous_repairs': previous_repairs})