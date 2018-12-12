from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, created_at, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            created_at=created_at,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, created_at, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            created_at=created_at,
            username=email,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=False
    )
    username = models.CharField(unique=True, null=False,max_length=255)
    created_at = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['created_at']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_email_field_name(self):
        return self.email
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class blog(models.Model):
    username = models.CharField(null=False, max_length=255)
    pub_date = models.DateTimeField(u"发布日期",auto_now_add = True,editable=True)       #博客发布日期
    content = models.TextField(blank=True, null=True)  # 博客文章正文
    like = models.IntegerField(default=0)

    def __unicode__(self):
        return self.username

class follow(models.Model):
    follow_friend = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='follow_friend')
    fans = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='fans')

class like(models.Model):
    username = models.CharField(null=False, max_length=255)
    likeblog = models.IntegerField()