from PIL import Image
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey("User",
                             on_delete=models.CASCADE)  # models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to="media/images/persons/")
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class UserManager(BaseUserManager):
    def create_user(self, email, name=None, branch=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, branch=branch, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        branch = None
        name = 'admin'
        return self.create_user(email, name, branch, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    pass
    # email = models.EmailField(unique=True)
    # name = models.CharField(max_length=255)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    branch = models.ForeignKey("Branch", on_delete=models.CASCADE, blank=True, null=True)
    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     blank=True,
    #     related_name='user_groups',
    #     related_query_name='user',
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     blank=True,
    #     related_name='user_permissions',
    #     related_query_name='user',
    # )
    #
    # objects = UserManager()
    #
    # USERNAME_FIELD = 'email'
    #
    # def __str__(self):
    #     return self.email
    #
    # def get_full_name(self):
    #     return self.name
    #
    # def get_short_name(self):
    #     return self.name.split()[0]


class Branch(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name
