from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from .utils import generate_ref_code
# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValidError("email is required")
        if not first_name:
            raise ValidError("First Name is required")
        if not last_name:
            raise ValidError("Last Name is required")

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            password = password
        )
        user.is_admin=True
        user.is_superuser = True
        user.is_staff =True
        user.save(using = self._db)
        return user


class MyUser(AbstractBaseUser):
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    email = models.EmailField(verbose_name="email address", max_length=60, unique=True)
    first_name = models.CharField(verbose_name="First Name", null=True, blank=True, max_length=100)
    middle_name = models.CharField(verbose_name="Middle Name", null=True, blank=True, max_length=100)
    last_name = models.CharField(verbose_name="Last Name", null=True, blank=True, max_length=100)
    phone = models.CharField(verbose_name="Contact Number", validators = [phoneNumberRegex], max_length=10, null=True, blank=True)
    city = models.CharField(verbose_name="City" ,max_length=100, null=True, blank=True)
    college = models.CharField(verbose_name="College", max_length=100, null=True, blank=True)
    facebook = models.URLField(verbose_name="Facebook Profile Link", max_length=100, null=True, blank=True)
    linkedin = models.URLField(verbose_name="Linked Profile Link", max_length=100, null=True, blank=True)
    image = models.ImageField(verbose_name="Upload Profile Picture", null=True, blank=True, upload_to='images')
    code = models.CharField(max_length=12, null=True, blank=True)
    count = models.IntegerField(null = True, blank= True, default=0)
    rank = models.IntegerField(null=True, blank=True, default=0)
    # customer = models.ManyToManyField(Customer)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class Customer(models.Model):
    name = models.CharField(max_length=200, null=True, blank = True)
    # first_name = models.CharField(max_length=200, null=True, blank = True)
    # last_name = models.CharField(max_length=200, null = True, blank = True)
    email = models.CharField(max_length=40, null=True)
    # phone = models.BigIntegerField(null=True, blank=True)
    # password = models.CharField(max_length=200, null=True)
    ambassador = models.ForeignKey(MyUser, null=True, blank=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, null=True, blank=True) 

    def __str__(self):
        return self.name
    
    # def get_recommend_profiles(self):
    #     pass
    
    # def save(self, *args, **kwargs):
    #     if self.code == "":
    #         code = generate_ref_code()
    #         self.code = code
    #         print(Yes)
        
    #     super().save(*args, **kwargs)