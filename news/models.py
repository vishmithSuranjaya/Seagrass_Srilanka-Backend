from django.db import models
from admin_actions.models import Admin
from media.models import Media

class News(models.Model):
    #this model is for the news articles on the weibsite
    news_id =models.CharField(max_length=10, primary_key = True)
    title = models.CharField(max_length =200)
    content =models.TextField(max_length =500)
    date = models.DateField()
    media_id = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, to_field='media_id')
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE, to_field='admin_id')
    
    def __str__(self):
        return f"News {self.news_id}"
    
    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"