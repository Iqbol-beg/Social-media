from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('get_all_users/', views.UserAPIView.as_view()),
    path( 'register/', views.RegisterApiView.as_view(), name='register'),
    path('login/',views.LoginApiView.as_view(), name="login"),
    
    # Post
    path('get_all_post/', views.PostListApiView.as_view()),
    path('create-post/',views.PostApiview.as_view()),
    path('read-post/', views.ReadPostApiView.as_view(), name='post-read'),
    path('update-post/<int:id>/', views.UpdatePostApiView.as_view(), name='post-update'),
    path('delete-post/<int:id>/', views.DeletePostApiView.as_view(), name='post-delete'),
    
    # Followers
    path('get_all_friend_requests/', views.FollowersListApiView.as_view(), name='followers-list'),
    path('friend-request/', views.FriendRequestAPIView.as_view(), name='friend-request'),
    path('accept-friend-request/', views.AcceptFriendRequestAPIView.as_view(), name='accept-friend-request'),

    # Comment
    path('add_comment/', views.AddCommentApiview.as_view(), name = 'add_comment'),
    path('get_all_posts_comment/<int:id>/', views.CommentListAPIView.as_view(), name='comment-list'),

    # Like
    path('add_like/', views.AddLikeApiView.as_view(), name = 'add_like'),
    path('get_users_who_liked/<int:post_id>/', views.WhoLikedApiView.as_view(), name = 'who_liked'),
]