from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User

class CustomUserManager(BaseUserManager):
    def create_user(self, matric_number, surname, password=None):
        if not matric_number:
            raise ValueError("The Matric Number field is required")
        if not surname:
            raise ValueError("The Surname field is required")

        user = self.model(matric_number=matric_number, surname=surname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matric_number, surname, password=None):
        user = self.create_user(matric_number, surname, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    matric_number = models.CharField(max_length=20, unique=True)
    surname = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'matric_number'
    REQUIRED_FIELDS = ['surname']

    def __str__(self):
        return self.matric_number

    @property
    def is_staff(self):
        return self.is_admin

class Exam(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=100)

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)




# Create your models here.
