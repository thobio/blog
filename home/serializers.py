from rest_framework import serializers
from .models import Blog
from django.contrib.auth.models import User


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        exclude = ["created_at", "updated_at"]
        depth = 1
