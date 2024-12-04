from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.exceptions import ValidationError


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    def update_followers_count(self):
        self.followers_count = Follow.objects.filter(following=self.user).count()
        self.save()


class Hashtag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    photo_post = models.ImageField(upload_to='img/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hashtags = models.ManyToManyField(Hashtag, related_name='posts', blank=True)
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"

    def toggle_like(self, user):
        """
        Adds or removes a like for the given user.
        """
        like, created = Like.objects.get_or_create(user=user, post=self)
        if not created:
            like.delete()  # If the like already exists, it is removed
        return created

    def likes_count(self):
        """
        Returns the number of likes associated with the post.
        """
        return self.like_set.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} commented: {self.content[:20]}"

    def clean(self):
        if not self.content.strip():
            raise ValidationError("The comment content cannot be empty.")
        if len(self.content) > 500:
            raise ValidationError("The comment cannot exceed 500 characters.")


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.following.profile.update_followers_count()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.following.profile.update_followers_count()
