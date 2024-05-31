from django import forms
from .models import Exam, Question

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['exam', 'text', 'option1', 'option2', 'option3', 'option4', 'correct_option']
