from django.db import models
from admin_actions.models import Admin
import uuid

def generate_uuid():
    return str(uuid.uuid4())


class Research_articles(models.Model):
    #this model is for the research articles on the website
    research_id = models.CharField(max_length =50, primary_key=True, default=generate_uuid, editable=False)
    link = models.CharField(max_length=200)
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE, to_field='admin_id')
    description = models.CharField(max_length=10000)  
    title = models.CharField(max_length=200)


    def __str__(self):
        return f"Reseach Article {self.research_id}"
    
    class Meta:
        verbose_name = "Research Article"
        verbose_name_plural = "Research Articles"

