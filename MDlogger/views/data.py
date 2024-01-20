from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.utils import OperationalError
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import F
from datetime import datetime, timedelta
from ..models import SavedRepair
import pandas as pd
import xlsxwriter

def data(request):
    sort_by = request.GET.get('sort_by', 'date')
    start_date_param = request.GET.get('start_date')
    end_date_param = request.GET.get('end_date')

    ninety_days_ago = datetime.now() - timedelta(days=90)
    start_date_default = ninety_days_ago.replace(hour=0, minute=0, second=0)
    end_date_default = datetime.now().replace(hour=23, minute=59, second=59) 
    
    try:
        start_date = datetime.strptime(start_date_param, "%Y-%m-%d") if start_date_param else start_date_default
        end_date = datetime.strptime(end_date_param, "%Y-%m-%d") if end_date_param else end_date_default
    except ValueError as e:
        messages.error(request, "Incorrect date format. Please use YYYY-MM-DD.")
        start_date, end_date = start_date_default, end_date_default  # Fallback to defaults
    
    formatted_start_date = start_date.strftime("%m-%d-%Y")
    formatted_end_date = end_date.strftime("%m-%d-%Y")
    repairs = SavedRepair.objects.select_related('user')


    try:
        if start_date and end_date:
            repairs = repairs.filter(date__range=(start_date, end_date))

        repairs = repairs.order_by(sort_by)
        repairs_count = repairs.count()
        export_queryset = repairs

        page = request.GET.get('page', 1)
        paginator = Paginator(repairs, 10)
        try:
            repairs = paginator.page(page)
        except PageNotAnInteger:
            repairs = paginator.page(1)
        except EmptyPage:
            repairs = paginator.page(paginator.num_pages)
    except OperationalError as e:
        return JsonResponse({'error': 'Database error'}, status=500)
    except PageNotAnInteger:
        repairs = paginator.page(1)
    except EmptyPage:
        repairs = paginator.page(paginator.num_pages)

    context = {
        'repairs': repairs,
        'repairs_count': repairs_count,
        'formatted_start_date': formatted_start_date,
        'formatted_end_date': formatted_end_date,
    }

    export_to_excel = request.GET.get('export_to_excel')
    if export_to_excel:
        try:
            df = pd.DataFrame(list(export_queryset.values('id', 'date', 'time', 'user__username', 'sku', 'lp', 'repair')))
            df.columns = ['Repair ID', 'Date', 'Time', 'User', 'SKU', 'LP', 'Repair']
            df['Time'] = df['Time'].apply(lambda x: x.strftime("%I:%M %p"))
    
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=repairs_data.xlsx'
            column_widths = {'A': 12, 'B': 15, 'C': 22, 'D': 15, 'E': 15, 'F': 30, 'G': 50}
            with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
                workbook = writer.book
                worksheet = writer.sheets['Sheet1']
                for col, width in column_widths.items():
                    worksheet.set_column(col + ':' + col, width)
            cell_format = workbook.add_format({'align': 'center'})
            worksheet.set_column('A:G', cell_format)
            
        except Exception as e:
            return JsonResponse({'error': 'Error exporting file from DataFrame'}, status=500)
        return response
    return render(request, 'MDlogger/data.html', context)
