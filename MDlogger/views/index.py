from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render

def index(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('MDlogger:index')
    else:
        form = AuthenticationForm()
    return render(request, 'MDlogger/index.html', {'form': form})