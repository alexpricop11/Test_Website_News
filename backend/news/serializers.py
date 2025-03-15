from rest_framework import serializers
from news.models import News, Comment, SavedNews
from users.models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "username"]


class NewsSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Users.objects.all(), source="author", write_only=True
    )
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ["id", "title", "slug", "author", "author_id", "content", "image",
                  "published_at", "updated_at", "is_published", "is_saved"]
        read_only_fields = ["published_at", "updated_at", "slug", "is_saved"]

    @staticmethod
    def validate_title(value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            exists = SavedNews.objects.filter(user=request.user, news=obj).exists()
            return exists
        return False


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=Users.objects.all(), source="user", write_only=True
    )

    class Meta:
        model = Comment
        fields = ["id", "news", "user", "user_id", "content", "created_at"]
        read_only_fields = ["created_at"]

    @staticmethod
    def validate_content(value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value


class SavedNewsSerializer(serializers.ModelSerializer):
    news_title = serializers.CharField(source='news.title', read_only=True)
    news_id = serializers.IntegerField(source='news.id', read_only=True)
    user = UserSerializer(read_only=True)
    news = NewsSerializer(read_only=True)

    class Meta:
        model = SavedNews
        fields = ['id', 'news_id', 'news_title', 'news', 'saved_at', 'user']
        read_only_fields = ['saved_at', 'user']
