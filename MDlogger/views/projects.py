from django.shortcuts import redirect, render
from ..models import  Projects
from ..forms import ProjectsForm

def projects(request):
    projects = Projects.objects.all()
    form = ProjectsForm()
    if request.method == 'POST':
        form = ProjectsForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('MDlogger:projects')
    else:
        form = ProjectsForm()
    return render(request, 'MDlogger/projects.html', {'projects': projects, 'form': form})