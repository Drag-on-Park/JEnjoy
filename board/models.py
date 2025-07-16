from django.db import models
from user.models import User
# Create your models here.


# class PostImage(models.Model):
#     image_url = models.ImageField(upload_to='post_images/', blank=True, null=True)
#     image_order = models.IntegerField()
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Tag(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()

    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title

