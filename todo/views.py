from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response

from .models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of tasks for the authenticated user.",
        parameters=[
            OpenApiParameter(name="status", description="Filter tasks by status.", required=False, type=str),
            OpenApiParameter(name="search", description="Search tasks by title or description.", required=False, type=str),
            OpenApiParameter(name="ordering", description="Order tasks by created_at or status.", required=False, type=str),
        ],
        examples=[
            OpenApiExample(
                "Example Request",
                value={},
                description="Request to list tasks.",
                request_only=True
            ),
            OpenApiExample(
                "Example Response",
                value=[
                    {
                        "id": 1,
                        "title": "Some task",
                        "description": "Description to make things clear",
                        "status": "in_progress",
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z",
                        "user": 1
                    }
                ],
                response_only=True
            )
        ]
    ),
    retrieve=extend_schema(
        description="Retrieve a specific task by ID.",
        examples=[
            OpenApiExample(
                "Example Response",
                value={
                    "id": 1,
                    "title": "Some task",
                    "description": "Description to make things clear",
                    "status": "in_progress",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                    "user": 1
                },
                response_only=True
            )
        ]
    ),
    create=extend_schema(
        description="Create a new task.",
        examples=[
            OpenApiExample(
                "Example Request",
                value={
                    "title": "Some task",
                    "description": "Description to make things clear",
                    "status": "in_progress"
                },
                request_only=True
            ),
            OpenApiExample(
                "Example Response",
                value={
                    "id": 1,
                    "title": "Some task",
                    "description": "Description to make things clear",
                    "status": "in_progress",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                    "user": 1
                },
                response_only=True
            )
        ]
    ),
    update=extend_schema(
        description="Update an existing task.",
        examples=[
            OpenApiExample(
                "Example Request",
                value={
                    "title": "Some updated task",
                    "description": "New description!",
                    "status": "completed"
                },
                request_only=True
            ),
            OpenApiExample(
                "Example Response",
                value={
                    "id": 1,
                    "title": "Some updated task",
                    "description": "New description!",
                    "status": "completed",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                    "user": 1
                },
                response_only=True
            )
        ]
    ),
    partial_update=extend_schema(
        description="Partially update an existing task.",
        examples=[
            OpenApiExample(
                "Example Request",
                value={
                    "status": "completed"
                },
                request_only=True
            ),
            OpenApiExample(
                "Example Response",
                value={
                    "id": 1,
                    "title": "Some task",
                    "description": "Description to make things clear",
                    "status": "completed",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                    "user": 1
                },
                response_only=True
            )
        ]
    ),
    destroy=extend_schema(
        description="Delete a task.",
        examples=[
            OpenApiExample(
                "Example Response",
                value={},
                description="Response after deleting a task.",
                response_only=True
            )
        ]
    )
)
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "status"]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of comments for a specific task.",
        examples=[
            OpenApiExample(
                "Example Response",
                value=[
                    {
                        "id": 1,
                        "text": "This is a comment on the task.",
                        "created_at": "2024-01-01T00:00:00Z",
                        "user": 1
                    }
                ],
                response_only=True
            )
        ]
    ),
    retrieve=extend_schema(
        description="Retrieve a specific comment by ID.",
        examples=[
            OpenApiExample(
                "Example Response",
                value={
                    "id": 1,
                    "text": "This is a comment on the task.",
                    "created_at": "2024-01-01T00:00:00Z",
                    "user": 1
                },
                response_only=True
            )
        ]
    ),
    create=extend_schema(
        description="Create a new comment for a specific task.",
        examples=[
            OpenApiExample(
                "Example Request",
                value={
                    "text": "This is a new comment."
                },
                request_only=True
            ),
            OpenApiExample(
                "Example Response",
                value={
                    "id": 1,
                    "text": "This is a new comment.",
                    "created_at": "2024-01-01T00:00:00Z",
                    "user": 1
                },
                response_only=True
            )
        ]
    ),
    update=extend_schema(
        description="Update an existing comment.",
        examples=[
            OpenApiExample(
                "Example Request",
                value={
                    "text": "This is an updated comment."
                },
                request_only=True
            ),
            OpenApiExample(
                "Example Response",
                value={
                    "id": 1,
                    "text": "This is an updated comment.",
                    "created_at": "2024-01-01T00:00:00Z",
                    "user": 1
                },
                response_only=True
            )
        ]
    ),
    partial_update=extend_schema(
        description="Partially update an existing comment.",
        examples=[
            OpenApiExample(
                "Example Request",
                value={
                    "text": "This is a partially updated comment."
                },
                request_only=True
            ),
            OpenApiExample(
                "Example Response",
                value={
                    "id": 1,
                    "text": "This is a partially updated comment.",
                    "created_at": "2024-01-01T00:00:00Z",
                    "user": 1
                },
                response_only=True
            )
        ]
    ),
    destroy=extend_schema(
        description="Delete a comment.",
        examples=[
            OpenApiExample(
                "Example Response",
                value={},
                response_only=True
            )
        ]
    )
)
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs["task_id"])

    def create(self, request, *args, **kwargs):
        task_id = self.kwargs["task_id"]
        if not Task.objects.filter(id=task_id).exists():
            return Response(
                {"detail": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            task_id=self.kwargs["task_id"]  # Set task_id directly
        )