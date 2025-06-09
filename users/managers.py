from django.contrib.auth.models import BaseUserManager
import uuid

class CustomUserManager(BaseUserManager):
    # custom user manager for JWT Authentication 

    def create_user(self, email, fname , lname, password = None , **extra_fields):
        if not email:
            raise ValueError("The Email Field must not be Empty")
        
        email = self.normalize_email(email)

        user_id = str(uuid.uuid4())[:10] # this is for creating a unique user_id

        user = self.model(
            email = email,
            fname = fname, 
            lname = lname,
            user_id = user_id,
            **extra_fields

        )
        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    def create_superuser(self, email, fname, lname, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser = True.")
        
        return self.create_user(email, fname, lname, password, **extra_fields)
    
    