from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from news.manager.comment import CommentManager
from news.manager.news import NewsManager
from news.manager.saved_news import SavedNewsManager
from news.models import News, SavedNews, Comment
from news.serializers import NewsSerializer, CommentSerializer, SavedNewsSerializer


class NewsListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = NewsSerializer

    def get(self, request):
        news = NewsManager.get_all_news()
        serializer = self.serializer_class(news, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyNewsListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = NewsSerializer

    def get(self, request):
        news = NewsManager.get_by_user(request.user.id)
        serializer = self.serializer_class(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NewsDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = NewsSerializer

    def get(self, request, news_id):
        news = NewsManager.get_by_id(news_id=news_id)
        if not news:
            return Response({"error": "News not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(news)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, news_id):
        news = NewsManager.get_by_id(news_id=news_id)
        if not news:
            return Response({"error": "News not found"}, status=status.HTTP_404_NOT_FOUND)
        if news.author != request.user:
            raise PermissionDenied("You cannot edit this news.")
        serializer = self.serializer_class(news, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, news_id):
        news = NewsManager.get_by_id(news_id=news_id)
        if not news:
            return Response({"error": "News not found"}, status=status.HTTP_404_NOT_FOUND)
        if news.author != request.user:
            raise PermissionDenied("You cannot delete this news.")
        NewsManager.delete(news_id=news_id)
        return Response({"message": "News deleted"}, status=status.HTTP_204_NO_CONTENT)


class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = CommentSerializer

    def get(self, request):
        news_id = request.query_params.get("news_id")
        if not news_id:
            return Response({"error": "news_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        comments = CommentManager.get_by_news(news_id)
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        comment_id = request.data.get('comment_id')
        if not comment_id:
            return Response({"error": "comment_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user != request.user:
            raise PermissionDenied("You cannot delete this comment.")

        CommentManager.delete(comment_id)
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class SavedNewsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = SavedNewsSerializer

    def post(self, request):
        news_id = request.data.get('news_id')
        if not news_id:
            return Response({"error": "news_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            saved_news, created = SavedNewsManager.save_news(user=request.user, news_id=news_id)
            serializer = self.serializer_class(saved_news)
            return Response(
                {
                    "message": "News saved successfully" if created else "News already saved",
                    "data": serializer.data,
                    "is_saved": True
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            saved_news = SavedNewsManager.get_saved_news(user=request.user)
            serializer = self.serializer_class(saved_news, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        news_id = request.data.get('news_id')
        if not news_id:
            return Response({"error": "news_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            SavedNewsManager.unsave_news(user=request.user, news_id=news_id)
            return Response({"message": "News unsaved successfully", "is_saved": False},
                            status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
