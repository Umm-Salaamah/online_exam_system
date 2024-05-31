from django.contrib import admin
from .models import Exam
from .models import Question
from .models import CustomUser



admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(CustomUser)


# Register your models here.
