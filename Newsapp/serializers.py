from.models import Blog
from rest_framework import serializers

class BlogSerializer(serializers.Serializer):
    key = serializers.IntegerField()
    email = serializers.EmailField()
    title = serializers.CharField()
    content = serializers.CharField()
    from datetime import datetime
    date = serializers.DateField(default=datetime.now)

    def create(self, validated_data):
        return Blog.objects.create(**validated_data)

    def update(self, blog, validated_data):
        newBlog = Blog(**validated_data)
        newBlog.id = blog.id
        newBlog.save()
        return newBlog
