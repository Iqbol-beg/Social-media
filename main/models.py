import random
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    avatar = models.ImageField(upload_to='image/', blank=True, null=True)

    def __str__(self):
        return self.username
    
 
    def clean_username(self):
        if not self.username:
            temp_username = f'Social-{str(uuid.uuid4()).split("-")[-1]}' 
            while User.objects.filter(username=temp_username).exists():
                temp_username = f"Social-{str(uuid.uuid4()).split('-')[-1]}{random.randint(0,9)}"
            self.username = temp_username

    def clean_password(self):
        if not self.password:
            self.password = f'Social-{str(uuid.uuid4()).split("-")[-1]}' 
           

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh_token": str(refresh)
        }

    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)

    def clean(self):
        self.clean_username()
        self.clean_password()
        self.hashing_password()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Followers(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to')

    def __str__(self):
        return f"{self.from_user.username} - {self.to_user.username}"
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    Comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
