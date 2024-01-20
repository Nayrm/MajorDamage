from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime, timedelta, date
from ..models import SavedRepair, Projects
from ..forms import AddRepairForm, ProjectsForm
import pandas as pd
import xlsxwriter
from django.db.models import Q
from django.http import JsonResponse
from django import forms
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

    
def metrics(request):  
    return render(request, 'MDlogger/metrics.html')
