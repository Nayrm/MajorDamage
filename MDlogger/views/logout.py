from django.shortcuts import render
from django.contrib.auth import logout

def logout_request(request):
    logout(request)
    return render(request, 'MDlogger/logout.html')