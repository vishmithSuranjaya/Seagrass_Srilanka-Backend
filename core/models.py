from django.db import models
from admin_actions.models import Admin

def gallery_image_upload_path(instance, filename):
    return f'gallery/{filename}'


class Gallery_images(models.Model):
    #this is for storing images and videos 
    image_id = models.CharField(max_length=10, primary_key = True)
    uploaded_at = models.DateTimeField(auto_now_add=True) 
    image = models.ImageField(upload_to=gallery_image_upload_path, blank=True, null=True, default=None)
    caption = models.CharField(max_length=100)
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE, to_field='admin_id')

    def __str__(self):
        return f"{self.caption} - {self.image_id}"
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"