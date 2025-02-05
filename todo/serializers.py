from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

from .models import Task, Comment
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Task Example',
            value={
                'title': 'Some task',
                'description': 'Description to make things clear',
                'status': 'in_progress'
            },
            request_only=True
        ),
        OpenApiExample(
            'Task Response Example',
            value={
                'id': 1,
                'title': 'Some task',
                'description': 'Description to make things clear',
                'status': 'in_progress',
                'created_at': '2024-01-01T00:00:00Z',
                'updated_at': '2024-01-01T00:00:00Z',
                'user': 1
            },
            response_only=True
        )
    ]
)
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(_("Title must be at least 3 characters long."))
        return value


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Comment Request Example',
            value={
                'text': 'Some comment'
            },
            request_only=True
        ),
        OpenApiExample(
            'Comment Response Example',
            value={
                'id': 1,
                'text': 'This is a comment on the task.',
                'created_at': '2024-01-01T00:00:00Z',
                'user': 1
            },
            response_only=True
        )
    ]
)
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'user', 'created_at')
        read_only_fields = ('user', 'created_at')

