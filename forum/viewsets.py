from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ForumPost,ForumPostBookmark
from .serializers import ForumPostSerializer,ForumPostBookmarkSerializer
from django.db.models import Count

class ForumPostViewSet(viewsets.ModelViewSet):
    queryset = ForumPost.objects.annotate(bookmark_count=Count('bookmarks')).order_by('-timestamp')
    serializer_class = ForumPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], url_path='bookmark')
    def bookmark(self, request, pk=None): #for toggling bookmark
        user = request.user
        post = self.get_object()

        bookmark, created = ForumPostBookmark.objects.get_or_create(user=user, post=post)

        if not created:
            bookmark.delete()
            return Response({'bookmarked': False}, status=status.HTTP_200_OK)

        return Response({'bookmarked': True}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='is-bookmarked')
    def is_bookmarked(self, request, pk=None): #for checking bookmark status
        post = self.get_object()
        is_bookmarked = ForumPostBookmark.objects.filter(user=request.user, post=post).exists()
        return Response({'bookmarked': is_bookmarked}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='bookmarked')
    def bookmarked(self, request):
        bookmarks = ForumPostBookmark.objects.filter(user=request.user)
        posts = [b.post for b in bookmarks]
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)