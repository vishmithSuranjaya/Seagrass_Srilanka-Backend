import os
from django.db import models
from users.models import Users
from admin_actions.models import Admin
from users.models import Users
from django.utils import timezone

def blog_image_upload_path(instance, filename):
    return f'blogs/{filename}'

# Create your models here.
class Blog(models.Model):
    #blog post model
    blog_id = models.CharField(max_length=10, primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, to_field='user_id')
    like_count = models.IntegerField(default=0)
    title = models.CharField(max_length=200, default="Untitled Blog")
    content = models.TextField(max_length=5000)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    status = models.CharField(max_length=15, default="active")
    comment_id = models.CharField(max_length=20, blank=True, null=True, default=None)
    image = models.ImageField(upload_to=blog_image_upload_path, blank=True, null=True, default=None)
    admin_id = models.ForeignKey( Admin,  on_delete=models.SET_NULL, to_field='admin_id', null=True, blank=True, default=None)
    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
    
    
    
class Comments(models.Model):
    #blog post comments model
    comment_id = models.CharField(max_length=20, primary_key =True)
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE, to_field='blog_id')
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, to_field='user_id')
    content = models.TextField(max_length=500)
    status = models.CharField(max_length = 15)
    type = models.CharField(max_length = 30)

    def __str__(self):
        return f"Comment by {self.user_id} on {self.blog_id}"
  