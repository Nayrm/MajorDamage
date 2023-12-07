from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime, timedelta, date
from .models import SavedRepair, Projects
from .forms import AddRepairForm, ProjectsForm
import pandas as pd
import xlsxwriter
from django.db.models import Q
from django.http import JsonResponse
from django import forms
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect







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

    projects = Projects.objects.filter(user=request.user, date=current_date, assignedto = request.user, status="Incomplete").order_by('-date')


    return render(request, 'MDlogger/associate_home.html', {'repairs': repairs,'pieces_repaired_today': pieces_repaired_today , 'projects': projects})

def mark_project_complete(request, project_id):
    project = get_object_or_404(Projects, id=project_id)

    # Update the status of the project to 'Complete' (or your desired status)
    project.status = 'Completed'
    project.save()

    # Redirect back to the home page or any other desired page
    return HttpResponseRedirect(reverse('MDlogger:associate_home'))

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

def metrics(request):  
    return render(request, 'MDlogger/metrics.html')



def data(request):
    sort_by = request.GET.get('sort_by', 'date')
    start_date_param = request.GET.get('start_date')
    end_date_param = request.GET.get('end_date')

    ninety_days_ago = datetime.now() - timedelta(days=90)
    start_date_default = ninety_days_ago.replace(hour=0, minute=0, second=0)
    end_date_default = datetime.now().replace(hour=23, minute=59, second=59)

    start_date = datetime.strptime(start_date_param, "%Y-%m-%d") if start_date_param else start_date_default
    end_date = datetime.strptime(end_date_param, "%Y-%m-%d") if end_date_param else end_date_default

    repairs = SavedRepair.objects.all()

    if start_date and end_date:
        repairs = repairs.filter(date__range=(start_date, end_date))

    repairs = repairs.order_by(sort_by)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(repairs, 10)  # Show 10 repairs per page
    try:
        repairs = paginator.page(page)
    except PageNotAnInteger:
        repairs = paginator.page(1)
    except EmptyPage:
        repairs = paginator.page(paginator.num_pages)

    context = {
        'repairs': repairs,
        'paginator': paginator,
    }

    export_to_excel = request.GET.get('export_to_excel')
    if export_to_excel:
        # Retrieve the entire filtered list for export
        all_repairs = SavedRepair.objects.filter(date__range=(start_date, end_date)).order_by(sort_by)
        df = pd.DataFrame(list(all_repairs.values_list()), columns=['Repair ID','Date', 'Time', 'User', 'SKU', 'LP', 'Repair'])
        df['Time'] = df['Time'].apply(lambda x: x.strftime("%I:%M %p"))
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=repairs_data.xlsx'
        column_widths = {'A': 12, 'B': 15, 'C': 22, 'D': 15, 'E': 15, 'F': 30, 'G': 50}  # Adjust widths as needed

        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')

            # Access the XlsxWriter workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']

            # Apply the specified column widths
            for col, width in column_widths.items():
                worksheet.set_column(col + ':' + col, width)
        cell_format = workbook.add_format({'align': 'center'})
        worksheet.set_column('A:G', cell_format)
        return response
    return render(request, 'MDlogger/data.html', context)





def format_time_range(start_time, end_time):
    # Format the time range in AM/PM format
    formatted_start_time = datetime.strptime(start_time, "%H:%M").strftime("%I:%M %p")
    formatted_end_time = datetime.strptime(end_time, "%H:%M").strftime("%I:%M %p")
    return f"{formatted_start_time} - {formatted_end_time}"

def dashboard(request):
    current_date = datetime.today().date()
    time_ranges = [
        {'start': '06:00', 'end': '06:59'},
        {'start': '07:00', 'end': '07:59'},
        {'start': '08:00', 'end': '08:59'},
        {'start': '09:00', 'end': '09:59'},
        {'start': '10:00', 'end': '10:59'},
        {'start': '11:00', 'end': '11:59'},
        {'start': '12:00', 'end': '12:59'},
        {'start': '13:00', 'end': '13:59'},
        {'start': '14:00', 'end': '14:59'},
        {'start': '15:00', 'end': '15:59'},
        {'start': '16:00', 'end': '16:59'},
        {'start': '17:00', 'end': '17:59'},
        {'start': '18:00', 'end': '18:59'},
        {'start': '19:00', 'end': '19:59'},
        {'start': '20:00', 'end': '20:59'},
        {'start': '21:00', 'end': '21:59'},
        {'start': '22:00', 'end': '22:59'},
        {'start': '23:00', 'end': '23:59'},
        # Add more time ranges as needed
    ]

    # Initialize a list to store data for each time range
    dashboard_data = []

    for time_range in time_ranges:
        start_time = time_range['start']
        end_time = time_range['end']

        # Filter SavedRepair objects for the current date and time range
        repairs_in_range = SavedRepair.objects.filter(
            date=current_date,
            time__gte=start_time,
            time__lte=end_time
        )
         # Count the number of repairs in the current time range
        pieces_repaired = repairs_in_range.count()
        formatted_time_range = format_time_range(start_time, end_time)

        dashboard_data.append({
            'time_range': formatted_time_range,
            'pieces_repaired': pieces_repaired,
        })

    # Append total row to the dashboard_data list
    dashboard_data.append({
        'time_range': 'Total:',
        'pieces_repaired': 0,  # Placeholder, as it will be updated in JavaScript
    })

    # Update the DataFrame with the total row
    dashboard_df = pd.DataFrame(dashboard_data)

    return render(request, 'MDlogger/dashboard.html', {'dashboard_df': dashboard_df})


def projects(request):
    projects = Projects.objects.all()



    form = ProjectsForm()  # Instantiate the form outside the if block
    if request.method == 'POST':
        form = ProjectsForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('MDlogger:projects')
              # Redirect to the project list page after successful form submission
    else:
        form = ProjectsForm()

    
    return render(request, 'MDlogger/projects.html', {'projects': projects, 'form': form})