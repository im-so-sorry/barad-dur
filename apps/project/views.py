from rest_framework import viewsets

from apps.project.models import Project
from apps.project.serializers import ProjectSerializer


class ProjectModelView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
