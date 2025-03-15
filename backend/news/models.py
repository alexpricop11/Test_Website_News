from django.db import models
from django.utils.text import slugify
from users.models import Users


class News(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="news")
    content = models.TextField()
    image = models.ImageField(upload_to="news_images/%Y/%m/", blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-published_at"]
        indexes = [models.Index(fields=["slug"])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.news.title}"


class SavedNews(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='saved_news')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'news')

    def __str__(self):
        return f"{self.user.username} saved {self.news.title}"
