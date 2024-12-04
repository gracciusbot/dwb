from django import forms
from .models import Post, Comment, Hashtag, Profile
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    hashtags = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter hashtags separated by spaces'}))

    class Meta:
        model = Post
        fields = ['title', 'photo_post', 'hashtags']

    def clean_hashtags(self):
        hashtags = self.cleaned_data.get('hashtags')
        if hashtags:
            hashtags = [tag.strip() for tag in hashtags.split() if tag.strip()]
            return hashtags
        return []

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            hashtags = self.cleaned_data.get('hashtags')
            for tag in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(name=tag)
                post.hashtags.add(hashtag)
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content.strip():
            raise forms.ValidationError("The comment content cannot be empty.")
        if len(content) > 500:
            raise forms.ValidationError("The comment cannot exceed 500 characters.")
        return content

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'bio']

class UserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Senha')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar Senha')

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("As senhas não coincidem")
        return cleaned_data
