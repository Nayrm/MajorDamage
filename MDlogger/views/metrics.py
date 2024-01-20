from django.shortcuts import render
from django.shortcuts import redirect, render

def metrics(request):  
    return render(request, 'MDlogger/metrics.html')
