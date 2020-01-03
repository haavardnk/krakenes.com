from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Project
from projects.models import Category
from hitcount.models import HitCount
from hitcount.views import HitCountMixin


def projects(request):
    project_list = Project.objects.all().order_by('-id')
    paginator = Paginator(project_list, 4)

    page = request.GET.get('page')
    projects = paginator.get_page(page)
    return render(request, 'projects/projects.html', {'projects': projects}, {'range': range(projects.paginator.num_pages+1)})


def project_details(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    hit_count = HitCount.objects.get_for_object(project)
    HitCountMixin.hit_count(request, hit_count)

    return render(request, 'projects/project_details.html', {'project': project})
