from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
import uuid


class UserManager(BaseUserManager):
    def create_user(self, username: str, email: str = None, password: str = None, **extra_fields) -> "Users":
        if not username:
            raise ValueError("The Username field is required.")
        email = self.normalize_email(email) if email else None
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username: str, email: str, password: str = None, **extra_fields) -> "Users":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True or extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_staff=True and is_superuser=True.")
        return self.create_user(username, email, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20, unique=True, db_index=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self) -> str:
        return self.username

    class Meta:
        db_table = "users"
        indexes = [models.Index(fields=["username"])]
