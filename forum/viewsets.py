from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ForumPost, ForumComment, ForumReply
from .serializers import ForumPostSerializer, ForumCommentSerializer, ForumReplySerializer

class ForumViewSet(viewsets.ViewSet):
    
    # ----- View All Posts -----
    @action(detail=False, methods=['get'])
    def posts(self, request):
        posts = ForumPost.objects.all()
        serializer = ForumPostSerializer(posts, many=True)
        return Response(serializer.data)

    # ----- View One Post with ID -----
    @action(detail=True, methods=['get'])
    def post_detail(self, request, pk=None):
        try:
            post = ForumPost.objects.get(pk=pk)
            serializer = ForumPostSerializer(post)
            return Response(serializer.data)
        except ForumPost.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    # ----- Create a New Post -----
    @action(detail=False, methods=['post'])
    def create_post(self, request):
        serializer = ForumPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    # ----- View All Comments -----
    @action(detail=False, methods=['get'])
    def comments(self, request):
        comments = ForumComment.objects.all()
        serializer = ForumCommentSerializer(comments, many=True)
        return Response(serializer.data)

    # ----- Create Comment for a Post -----
    @action(detail=False, methods=['post'])
    def add_comment(self, request):
        serializer = ForumCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    # ----- View All Replies -----
    @action(detail=False, methods=['get'])
    def replies(self, request):
        replies = ForumReply.objects.all()
        serializer = ForumReplySerializer(replies, many=True)
        return Response(serializer.data)

    # ----- Create Reply for a Comment -----
    @action(detail=False, methods=['post'])
    def add_reply(self, request):
        serializer = ForumReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
