from django.db import models
from users.models import Users
from admin_actions.models import Admin
from user.models import User

# Create your models here.
class Blog(models.Model):
    #blog post model
    blog_id = models.CharField(max_length=10, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, to_field='user_id' )
    title = models.CharField(max_length=200)
    content = models.TextField(max_length = 1000)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length = 15)
    comment_id = models.CharField(max_length=20, blank = True, null = True)
    media_id = models.CharField(max_length=20, blank=True, null = True)
    admin_id = models.ForeignKey(Admin, on_delete=models.SET_NULL, to_field='admin_id', null=True, blank=True , default=None)

    def __str__(self):
        return self.title
    
    
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
  