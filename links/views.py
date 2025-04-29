from rest_framework import viewsets, permissions
from .models import Link
from .serializers import LinkSerializer
from django_filters.rest_framework import DjangoFilterBackend


class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['link_type']

    def get_queryset(self):
        return Link.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)