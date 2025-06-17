from django.db import models
from admin_actions.models import Admin
from django.utils import timezone
import uuid

def news_image_upload_path(instance, filename):
    return f'news/{filename}'


class News(models.Model):
    news_id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=2000)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 
    image = models.ImageField(upload_to=news_image_upload_path, blank=True, null=True)
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE, to_field='admin_id')
    is_published = models.BooleanField(default=True)  
    
    def __str__(self):
        return f"News: {self.title}"
    
    class Meta:
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"
        ordering = ['-created_at'] 