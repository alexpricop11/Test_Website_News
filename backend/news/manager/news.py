from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from news.models import News, Comment


class NewsManager:
    @staticmethod
    def get_by_id(news_id=None, slug=None):
        if news_id:
            return get_object_or_404(News.objects.select_related("author"), id=news_id)
        elif slug:
            return get_object_or_404(News.objects.select_related("author"), slug=slug)
        else:
            raise ValueError("Either news_id or slug must be provided.")

    @staticmethod
    def get_all_news():
        return News.objects.filter(is_published=True).select_related("author")

    @staticmethod
    def get_by_user(user_id):
        return News.objects.filter(author_id=user_id).select_related("author")

    @staticmethod
    def create(title, author, content, image=None, is_published=False):
        if not content.strip():
            raise ValidationError("Content cannot be empty.")
        return News.objects.create(title=title, author=author, content=content, image=image, is_published=is_published)

    @staticmethod
    def update(news, title=None, content=None, image=None, is_published=None):
        if title is not None:
            news.title = title
        if content is not None:
            news.content = content
        if image is not None:
            news.image = image
        if is_published is not None:
            news.is_published = is_published
        news.save()
        return news

    @staticmethod
    def delete(news_id=None, slug=None):
        news = NewsManager.get_by_id(news_id=news_id, slug=slug)
        news.delete()
