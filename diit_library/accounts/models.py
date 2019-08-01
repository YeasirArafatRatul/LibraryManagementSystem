from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, id_card_number, department, designation=None, phone=None,  batch=None, class_id=None,
                    password=None, is_active=True, is_staff=False, is_admin=False):
        # all the required fields must be passed as arguments
        if not email:
            raise ValueError("Put an email address")
        if not password:
            raise ValueError("Input a password")
        if not full_name:
            raise ValueError("You must add your fullname")
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )
        user.phone = phone
        user.id_card_number = id_card_number
        user.batch = batch
        user.class_id = class_id
        user.department = department
        #user.designation = "Student"
        user.set_password(password)

        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

        # user = user_object

    def create_staffuser(self, email, full_name, department, designation=None, phone=None, id_card_number=None, batch=None, class_id=None,
                         password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            phone=phone,
            designation=designation,

            is_staff=True
        )
        return user

    def create_superuser(self, email, full_name, department, id_card_number, designation=None,  phone=None,
                         batch=None, class_id=None,
                         password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            phone=phone,
            id_card_number=id_card_number,
            department=department,
            password=password,

            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=15)
    batch = models.IntegerField(null=True, blank=True)
    class_id = models.IntegerField(unique=True)  # , null=True, blank=True
    department = models.CharField(max_length=15)
    id_card_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.IntegerField(null=True, blank=True)
    # for the stuffs
    designation = models.CharField(max_length=15)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    # username & password is required by django default
    REQUIRED_FIELDS = ['full_name', 'phone', 'id_card_number', 'department']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_level):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class UserProfileManager(models.Manager):
    def profile_update(request, image):
        profile_update_obj = request.model(image=image)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.email}'

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)

    objects = UserProfileManager()

# signal.py
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        post_save.connect(create_profile, sender=User)
