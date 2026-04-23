from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from django.conf import settings
from django.db import models
from .models import Task
from .serializers import TaskSerializer, TaskCreateUpdateSerializer
from .filters import TaskFilter
from core.cache import generate_cache_key, invalidate_task_cache
from core.throttling import BurstRateThrottle, TaskCreateThrottle


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'priority', 'status']
    ordering = ['-created_at']
    throttle_classes = [BurstRateThrottle]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Task.objects.all().select_related('created_by', 'assigned_to')
        return Task.objects.filter(
            models.Q(created_by=user) | models.Q(assigned_to=user)
        ).select_related('created_by', 'assigned_to')
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return TaskCreateUpdateSerializer
        return TaskSerializer
    
    def get_throttles(self):
        """Apply different throttles based on action"""
        if self.action == 'create':
            return [TaskCreateThrottle()]
        return super().get_throttles()
    
    def list(self, request, *args, **kwargs):
        """List tasks with caching"""
        # Generate cache key based on user and query params
        cache_key = generate_cache_key(
            'task_list',
            user_id=request.user.id,
            params=str(request.query_params)
        )
        
        # Try to get from cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        # If not in cache, get from database
        response = super().list(request, *args, **kwargs)
        
        # Cache the response
        if response.status_code == 200:
            cache.set(cache_key, response.data, settings.CACHE_TTL['task_list'])
        
        return response
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve task with caching"""
        task_id = kwargs.get('pk')
        cache_key = f'task_detail:{task_id}'
        
        # Try to get from cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        # If not in cache, get from database
        response = super().retrieve(request, *args, **kwargs)
        
        # Cache the response
        if response.status_code == 200:
            cache.set(cache_key, response.data, settings.CACHE_TTL['task_detail'])
        
        return response
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        # Invalidate cache after creation
        invalidate_task_cache(user_id=self.request.user.id)
    
    def perform_update(self, serializer):
        instance = serializer.save()
        # Invalidate cache after update
        invalidate_task_cache(task_id=instance.id, user_id=self.request.user.id)
    
    def perform_destroy(self, instance):
        task_id = instance.id
        user_id = self.request.user.id
        instance.delete()
        # Invalidate cache after deletion
        invalidate_task_cache(task_id=task_id, user_id=user_id)
    
    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        """Get tasks assigned to current user with caching"""
        cache_key = f'user_tasks:{request.user.id}'
        
        # Try to get from cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        # If not in cache, get from database
        tasks = self.get_queryset().filter(assigned_to=request.user)
        page = self.paginate_queryset(tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = self.get_paginated_response(serializer.data).data
        else:
            serializer = self.get_serializer(tasks, many=True)
            response_data = serializer.data
        
        # Cache the response
        cache.set(cache_key, response_data, settings.CACHE_TTL['user_tasks'])
        
        return Response(response_data)
    
    @action(detail=False, methods=['get'])
    def created_by_me(self, request):
        """Get tasks created by current user"""
        tasks = self.get_queryset().filter(created_by=request.user)
        page = self.paginate_queryset(tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def mark_completed(self, request, pk=None):
        """Mark task as completed"""
        task = self.get_object()
        task.status = 'completed'
        task.save()
        
        # Invalidate cache
        invalidate_task_cache(task_id=task.id, user_id=request.user.id)
        
        serializer = self.get_serializer(task)
        return Response(serializer.data)
