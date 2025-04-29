from rest_framework import serializers
from .models import Link
from .parsers import parse_link_metadata


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = [
            'id', 'url', 'title',
            'description', 'image_url',
            'link_type', 'created_at',
            'updated_at', 'owner'
        ]
        read_only_fields = [
            'id', 'title', 'description',
            'image_url', 'link_type',
            'created_at', 'updated_at', 'owner'
        ]

    def create(self, validated_data):
        metadata = parse_link_metadata(validated_data['url'])
        validated_data.update(metadata)
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'url' in validated_data and instance.url != validated_data['url']:
            metadata = parse_link_metadata(validated_data['url'])
            validated_data.update(metadata)
        return super().update(instance, validated_data)