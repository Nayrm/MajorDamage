from django.shortcuts import render
from django.shortcuts import redirect, render
from datetime import datetime, timedelta, date
from ..models import SavedRepair, Projects
import pandas as pd

def format_time_range(start_time, end_time):
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
    ]

    dashboard_data = []

    for time_range in time_ranges:
        start_time = time_range['start']
        end_time = time_range['end']
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

    dashboard_data.append({
        'time_range': 'Total:',
        'pieces_repaired': 0,
    })

    dashboard_df = pd.DataFrame(dashboard_data)

    return render(request, 'MDlogger/dashboard.html', {'dashboard_df': dashboard_df})