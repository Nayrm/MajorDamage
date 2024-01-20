from ..models import Projects
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

def mark_project_complete(request, project_id):
    project = get_object_or_404(Projects, id=project_id)
    project.status = 'Completed'
    project.save()
    return HttpResponseRedirect(reverse('MDlogger:associate_home'))