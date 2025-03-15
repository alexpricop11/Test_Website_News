from django.core.exceptions import ValidationError
from news.models import News, SavedNews


class SavedNewsManager:
    @staticmethod
    def save_news(user, news_id):
        try:
            news = News.objects.get(id=news_id)
            saved_news, created = SavedNews.objects.get_or_create(user=user, news=news)
            return saved_news, created
        except News.DoesNotExist:
            raise ValidationError("News item not found")
        except Exception as e:
            raise ValidationError(str(e))

    @staticmethod
    def get_saved_news(user):
        return SavedNews.objects.filter(user=user).select_related('news')

    @staticmethod
    def unsave_news(user, news_id):
        try:
            saved_news = SavedNews.objects.get(user=user, news_id=news_id)
            saved_news.delete()
            return True
        except SavedNews.DoesNotExist:
            raise ValidationError("News not saved by this user")
        except Exception as e:
            raise ValidationError(str(e))
