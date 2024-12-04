from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import models
from .models import Post, Follow, Comment, Profile, Like, Hashtag
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from BlogApp.forms import ProfileForm, CommentForm, PostForm, UserForm
from django.contrib.auth import get_user_model
import logging


class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    login_url = '/login/'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Buscar todos os posts
        posts = Post.objects.all()
        
        # Atualizando o likes_count de cada post
        for post in posts:
            post.likes_count = post.like_set.count()  # Acessando a relação reversa 'like_set'
        
        context['posts'] = posts
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            posts_data = []
            for post in self.get_queryset():
                post_data = {
                    'id': post.id,
                    'title': post.title,
                    'author': post.author.username,
                    'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'photo_post': post.photo_post.url if post.photo_post else None,
                    'likes_count': post.likes_count,
                    'comments_count': post.comments_count,
                    'is_liked_by_user': post.is_liked_by_user,
                    'is_followed_by_user': post.is_followed_by_user
                }
                posts_data.append(post_data)

            return JsonResponse({'posts': posts_data})
        return super().get(request, *args, **kwargs)



class PostView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        context.update({
            'comments': post.comments.all(),
            'profile': post.author.profile,
            'is_following': Follow.objects.filter(follower=self.request.user, following=post.author).exists(),
            'likes_count': post.likes.count(),
        })
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            post = self.get_object()
            try:
                post_data = {
                    'id': post.id,
                    'title': post.title,
                    'author': post.author.username,
                    'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'photo_post': post.photo_post.url if post.photo_post else None,
                    'comments_count': post.comments.count(),
                    'author_photo' : post.author.profile.photo.url,
                    'is_following': Follow.objects.filter(follower=request.user, following=post.author).exists(),
                    'comments': list(post.comments.values('id', 'author__username', 'content', 'created_at')),
                }
                return JsonResponse(post_data)
            except Exception as e:
                logging.error(f"Error loading post details: {e}")
                return JsonResponse({'error': 'Error loading post details.'}, status=500)
        return super().get(request, *args, **kwargs)


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        liked = False

        if Like.objects.filter(user=request.user, post=post).exists():
            Like.objects.filter(user=request.user, post=post).delete()
        else:
            Like.objects.create(user=request.user, post=post)
            liked = True

        return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})


class ToggleFollowView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)

        if user_to_follow == request.user:
            return JsonResponse({'error': 'You cannot follow yourself.'}, status=400)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        is_following = created
        if not created:
            follow.delete()

        followers_count = Follow.objects.filter(following=user_to_follow).count()

        return JsonResponse({'is_following': is_following, 'followers_count': followers_count})


class SearchUserView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'search_user.html'
    context_object_name = 'users'
    login_url = '/login/'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return User.objects.filter(username__icontains=query) if query else User.objects.none()


class SearchPostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'search_post.html'
    context_object_name = 'posts'
    login_url = '/login/'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Post.objects.filter(title__icontains=query) if query else Post.objects.none()


class CreatePostView(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        return render(request, 'create_post.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully.')
            return redirect('home')
        return render(request, 'create_post.html', {'form': form})

class RegisterView(View):
    def get(self, request):
        user_form = UserForm()
        return render(request, 'register.html', {'user_form': user_form})

    def post(self, request):
        user_form = UserForm(request.POST)
        
        if user_form.is_valid():
            # Criar o usuário com as informações do formulário
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()

            # Criar o perfil associado ao usuário
            Profile.objects.create(user=user)

            messages.success(request, 'Registration successful.')
            return redirect('login')

        return render(request, 'register.html', {'user_form': user_form})




class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'
    login_url = '/login/'

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username).profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'posts': Post.objects.filter(author=self.object.user).order_by('-created_at'),
            'followers': Follow.objects.filter(following=self.object.user).count(),
            'following': Follow.objects.filter(follower=self.object.user).count(),
        })
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            profile = self.get_object()
            try:
                profile_data = {
                    'id': profile.id,
                    'username': profile.user.username,
                    'bio': profile.bio,
                    'profile_photo': profile.photo.url if profile.photo else None,
                    'followers_count': Follow.objects.filter(following=profile.user).count(),
                    'following_count': Follow.objects.filter(follower=profile.user).count(),
                    'posts_count': Post.objects.filter(author=profile.user).count(),
                    'is_following': Follow.objects.filter(follower=request.user, following=profile.user).exists(),
                    'posts': list(
                        Post.objects.filter(author=profile.user)
                        .order_by('-created_at')
                        .values('id', 'title', 'created_at', 'photo_post')
                    ),
                }
                return JsonResponse(profile_data)
            except Exception as e:
                logging.error(f"Error loading profile details: {e}")
                return JsonResponse({'error': 'Error loading profile details.'}, status=500)
        return super().get(request, *args, **kwargs)

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Aqui buscamos o usuário pelo email
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            user = None

        if user and user.check_password(password):
            login(request, user)
            return redirect('home')  # Redireciona para a home após o login
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')  # Redireciona para a página de login novamente




class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
