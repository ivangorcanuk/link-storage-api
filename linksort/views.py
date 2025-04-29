from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Collection, Link
from .serializers import CollectionSerializer, CollectionLinkSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def add_link(self, request, pk=None):
        collection = self.get_object()
        serializer = CollectionLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        link = get_object_or_404(Link, id=serializer.validated_data['link_id'], owner=request.user)

        collection.links.add(link)
        return Response(
            {'status': 'link added'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['delete'])
    def remove_link(self, request, pk=None):
        collection = self.get_object()
        serializer = CollectionLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        link = get_object_or_404(Link, id=serializer.validated_data['link_id'], owner=request.user)

        collection.links.remove(link)
        return Response(
            {'status': 'link removed'},
            status=status.HTTP_204_NO_CONTENT
        )