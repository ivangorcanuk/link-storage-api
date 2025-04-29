from rest_framework import serializers
from .models import Collection, Link
from LinkHub.links.serializers import LinkSerializer


class CollectionSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = [
            'id', 'name', 'description',
            'links', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'owner'
        ]


class CollectionLinkSerializer(serializers.Serializer):
    link_id = serializers.IntegerField()

    def validate_link_id(self, value):
        if not Link.objects.filter(id=value).exists():
            raise serializers.ValidationError("Link does not exist")
        return value