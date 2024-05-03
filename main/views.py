from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import   RegisterSerializer, UserSerializer, LoginSerializer, CreatePostSerialzer,AddCommentSerializer,CommentSerializer, AddLikeSerializer
from .serializers import FollowersSerializer,ReadPostSerializer,UpdatePostSerializer,PostSerializer,FollowSerializer,AcceptFollowRequestSerializer,LikeSerializer
from . import models
from rest_framework import status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        users = models.User.objects.all()
        if q:
            users.filter(
                Q(username__icontains=q)| 
                Q(first_name__iconatins=q)| 
                Q(last_name__iconatins=q)|
                Q(email__icontains=q)
                )
            
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class RegisterApiView(APIView):
    
      def post(self, request):
            user=request.user
            serializer=RegisterSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response (serializer.data)
    
class LoginApiView(APIView):
    def post(self, request):
        data=request.data
        serializer=LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user=authenticate(username=serializer.data['username'],)

        if user is None:
            data={
                'status': False,
                'message': "User not found"
            }
            return Response (data)
        refresh=RefreshToken.for_user(user)

        data={
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
        return Response (data)

# POST
class PostApiview(APIView):
     permission_classes ={IsAuthenticated,}
     
     def post(self, request):
          user = request.user
          data = {
               "contenet":request.data['content'],
               "user":user.id
          }
          serializer = CreatePostSerialzer(data=data)
          serializer.is_valid(raise_exception=True)
          return Response(serializer.data)
     
class ReadPostApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = models.Post.objects.all()
        serializer =ReadPostSerializer(posts, many=True)
        return Response(serializer.data)
    
class UpdatePostApiView(APIView):    
     def put(self, request, id):
        post = models.Post.objects.get(id=id)
        serializer = UpdatePostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class DeletePostApiView(APIView):
      def delete(self, request, id):
        post = models.Post.objects.filter(author = request.user).get(id = id)
        post.delete()
        return Response({'success':'post has been deleted'})
     

class PostListApiView(APIView):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        users = models.Post.objects.all()
        if q:
            users = users.filter(
                Q(username__icontains=q) | 
                Q(content__icontains=q) | 
                Q(Created_at__icontains=q) 
            )
        serializer = PostSerializer(users, many=True)
        return Response(serializer.data)
     


# Followers

class FollowersListApiView(APIView):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        users = models.Followers.objects.all()
        if q:
            users = users.filter(
                Q(from_user__icontains=q) | 
                Q(to_user__icontains=q) 
            )
        serializer = FollowersSerializer(users, many=True)
        return Response(serializer.data)
    

class FriendRequestAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = FollowSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(from_user=request.user)
        return Response({'success': 'Follow yuborildi'}, status=status.HTTP_201_CREATED)

class AcceptFriendRequestAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = AcceptFollowRequestSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(to_user=request.user)
        return Response({'success': 'Follow qabul qilindi'}, status=status.HTTP_200_OK)
    
    # Comment
class AddCommentApiview(APIView):
     permission_classes ={IsAuthenticated,}
     
     def post(self, request):
          user = request.user
          post_id = request.post_id
          data = {
               "comment":request.data['comment'],
               "user":user.id,
               "post_id":post_id.id
          }
          serializer = AddCommentSerializer(data=data)
          serializer.is_valid(raise_exception=True)
          return Response(serializer.data)
     
class CommentListAPIView(APIView):
    def get(self, request, id,*args, **kwargs):
        q = request.GET.get('q')
        comments = models.Comment.objects.filter(id=id)
        if q:
            comments = comments.filter(
                Q(post__id__icontains=q) |
                Q(comment__icontains=q)
            )
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    # Like
class AddLikeApiView(APIView):
     permission_classes ={IsAuthenticated,}
     
     def post(self, request):
          user = request.user
          post = request.post
          data = {
               "post":post.id,
               "user":user.id
          }
          serializer = AddLikeSerializer(data=data)
          serializer.is_valid(raise_exception=True)
          return Response(serializer.data)
     
class WhoLikedApiView(APIView):
    permission_classes = {IsAuthenticated}

    def get(self, request, post_id):
        q = request.GET.get('q')
        likes = models.Like.objects.filter(post_id=post_id)
        if q:
            likes = likes.filter(
                Q(username__icontains=q)| 
                Q(post__id__icontains=q) 
            )

        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)
    
