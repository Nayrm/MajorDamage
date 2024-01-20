from django.shortcuts import redirect, render
from django.contrib import messages
from datetime import datetime
from ..models import SavedRepair
from ..forms import AddRepairForm

def add_repair(request):
    lp = request.session.get('lp')
    sku = request.session.get('sku')
    
    if lp is None or sku is None:
        return redirect('MDlogger:associate_home')

    form = AddRepairForm() 

    if request.method == "POST":
        form = AddRepairForm(request.POST)

        if form.is_valid():
            date = datetime.now()
            time = request.POST.get('time')
            user_first_name = request.user.first_name
            user_last_name = request.user.last_name
            repair = form.cleaned_data['repair']
            SavedRepair.objects.create(
                date=date,
                time=time,
                user=request.user,
                sku=sku,
                lp=lp,
                repair=repair
            )
            messages.success(request, f"Repair for LP {lp} saved.")
            return redirect('MDlogger:associate_home')
    
    return render(request, 'MDlogger/add_repair.html', {'form': form, 'sku': sku, 'lp': lp})