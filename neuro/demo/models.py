from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        username = self.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_client(self, username, password):
        user = self.create_user(
            username,
            password=password,
        )
        user.client = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username,
            password=password,
        )
        user.admin = True
        user.save(using=self._db)
        return user

    def create_root(self, username, password):
        user = self.create_user(
            username,
            password=password,
        )
        user.client = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(models.Model):
    username = models.CharField(verbose_name='Логин', max_length=50)
    password = models.CharField(verbose_name='Пароль', max_length=50)
    is_active = models.BooleanField(
        ('active'),
        default=False,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'), )
    client = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    # user_created = models.DateTimeField(default=timezone.now)


class UserImages(models.Model):
    user_image = models.TextField(verbose_name='Фото')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user_image_created = models.DateTimeField(default=timezone.now)


class UserPartFace(models.Model):
    user_part_face = models.CharField(verbose_name='Часть лица', max_length=50)
    user_image = models.ForeignKey(UserImages, on_delete=models.CASCADE)


class UserShades(models.Model):
    user_shade = models.CharField(verbose_name='Оттенок', max_length=100)
    user_part_face = models.ForeignKey(UserPartFace, on_delete=models.CASCADE)


class Posts(models.Model):
    post_image = models.TextField(verbose_name='Фото')
    # created = models.DateTimeField(default=timezone.now)


class PartFace(models.Model):
    post_part_face = models.CharField(verbose_name='Часть лица', max_length=50)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)


class Shades(models.Model):
    post_shade = models.CharField(verbose_name='Оттенок', max_length=50)
    part_face = models.ForeignKey(PartFace, on_delete=models.CASCADE)
