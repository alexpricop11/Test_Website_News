from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from news.models import Comment


class CommentManager:
    @staticmethod
    def get_by_news(news_id):
        return Comment.objects.filter(news_id=news_id).select_related("user")

    @staticmethod
    def create(news, user, content):
        if not content.strip():
            raise ValidationError("Content cannot be empty.")
        return Comment.objects.create(news=news, user=user, content=content)

    @staticmethod
    def delete(comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
