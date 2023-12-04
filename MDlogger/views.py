from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from .models import SavedRepair
from .forms import AddRepairForm





# Create your views here.
def index(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('MDlogger:index')
    else:
        form = AuthenticationForm()
    return render(request, 'MDlogger/index.html', {'form': form})



def logout_request(request):
    logout(request)
    return render(request, 'MDlogger/logout.html')

def associate_home(request):
    current_date = datetime.now().date()
    repairs = SavedRepair.objects.filter(user=request.user, date=current_date).order_by('-date', '-time')
    pieces_repaired_today = len(repairs)
    return render(request, 'MDlogger/associate_home.html', {'repairs': repairs,'pieces_repaired_today': pieces_repaired_today})

def lp_entry(request):
    lp = None
    previous_repairs = None

    if request.method == "POST":
        lp = request.POST.get('lp')

        # Check if LP is saved for today
        if SavedRepair.objects.filter(lp=lp, date=datetime.now().date()).exists():
            # If LP has previous repairs, fetch and display them
            previous_repairs = SavedRepair.objects.filter(lp=lp, date=datetime.now().date())
        else:
            # If no previous repairs, proceed to the SKU entry page
            request.session['lp'] = lp
            return redirect('MDlogger:sku_entry')

    return render(request, 'MDlogger/lp_entry.html', {'lp': lp, 'previous_repairs': previous_repairs})

def sku_entry(request):
    lp = request.session.get('lp')
    if lp is None:
        return redirect('MDlogger:associate_home')
    if request.method == "POST":
        sku = request.POST.get('sku')
        request.session['sku'] = sku
        return redirect('MDlogger:add_repair')
    return render(request, 'MDlogger/sku_entry.html', {'lp': lp})
    

def add_repair(request):
    lp = request.session.get('lp')
    sku = request.session.get('sku')
    
    if lp is None or sku is None:
        return redirect('MDlogger:associate_home')

    form = AddRepairForm()  # Instantiate the form outside the if block

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