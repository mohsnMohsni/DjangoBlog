from rest_framework import serializers
from .models import Post, Category, Comment
from django.contrib.auth import get_user_model
from account.serializers import UserSerializer

User = get_user_model()


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=150)
    slug = serializers.SlugField()
    content = serializers.CharField(max_length=250)
    create_at = serializers.DateTimeField(read_only=True)
    update_at = serializers.DateTimeField(read_only=True)
    publish_time = serializers.DateTimeField()
    draft = serializers.BooleanField()
    image = serializers.ImageField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.content = validated_data.get('content', instance.content)
        instance.publish_time = validated_data.get('publish_time', instance.publish_time)
        instance.draft = validated_data.get('draft', instance.draft)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    author_detail = UserSerializer(source='author', read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
