from django.db import models
from django.db.models import Model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from PIL import Image

class UserManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError('User must have email address')
        if not username:
            raise ValueError('User must have username')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        user = self.create_user(
            email= self.normalize_email(email),
            password=password,
            username=username
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    
class Account(AbstractBaseUser):
    email                   = models.EmailField(verbose_name='email',max_length=60,unique=True)
    username                = models.CharField(max_length=30,unique=True)
    date_joined             = models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name='last login',auto_now=True)  
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)

    USERNAME_FIELD          = 'email'
    REQUIRED_FIELDS         = ['username']
    objects                 = UserManager()
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True

class Profile(models.Model):
    user                = models.OneToOneField(Account, on_delete=models.CASCADE)
    fname               = models.CharField(max_length=50,null=True)
    fullname            = models.CharField(max_length=50,null=True)    
    mobile              = models.IntegerField(null=True)
    tech_stack          = models.CharField(max_length=50,null=True)
    ASPIRANT = 1
    COACH = 2
    ROLE_CHOICES = (
        (ASPIRANT,'aspirant'),
        (COACH,'coach')
    ) 
    role                = models.PositiveSmallIntegerField(choices=ROLE_CHOICES,default=1)
    image               = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    
    def save(self, **kwargs):
        super().save()
        img= Image.open(self.image.path)

        if img.height>300 or img.width>300:
            output_size =(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.user.email

