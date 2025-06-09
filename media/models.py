from django.db import models
from users.models import Users
from admin_actions.models import Admin

class Media(models.Model):
    #this is for storing images and videos 
    media_id = models.CharField(max_length=20, primary_key = True)
    name = models.CharField(max_length = 50)
    link = models.CharField(max_length=200)
    type = models.CharField(max_length=30)
    user_id = models.ForeignKey(Users , on_delete=models.CASCADE, to_field='user_id')
    product_id = models.CharField(max_length=20, blank=True, null=True)
    admin_id =models.ForeignKey(Admin, on_delete=models.CASCADE, to_field='admin_id')

    def __str__(self):
        return self.name