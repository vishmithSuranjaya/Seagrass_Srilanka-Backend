from django.db import models

class Admin(models.Model):
    #system administrator model
    admin_id = models.CharField(max_length=10, primary_key=True)
    username = models.CharField(max_length=30, unique = True)
    password = models.CharField(max_length=100)
    type = models.CharField(max_length=30)

    def __str__(self):
        return self.username
    

