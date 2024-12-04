from django.urls import path
from .views import HomeView, LikePostView, PostView, ToggleFollowView, RegisterView, ProfileView, LoginView, LogoutView, SearchUserView, SearchPostView, CreatePostView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('like/<int:pk>/', LikePostView.as_view(), name='like_post'),
    path('post/<int:pk>/', PostView.as_view(), name='post_detail'),
    path('follow/<int:user_id>/', ToggleFollowView.as_view(), name='follow_user'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('search_user/', SearchUserView.as_view(), name='search_user'),
    path('search_post/', SearchPostView.as_view(), name='search_post'),
    path('create_post/', CreatePostView.as_view(), name='create_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
