from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exam, Question, Result
from .forms import ExamForm, QuestionForm
from django.db import connection
from .models import Exam
from django.contrib.auth import authenticate, login
from .models import CustomUser

#Sign-In View
def sign_in(request):
    if request.method == 'POST':
        matric_number = request.POST['matric_number']
        surname = request.POST['surname']
        try:
            user = CustomUser.objects.get(matric_number=matric_number, surname=surname)
            login(request, user)
            return redirect('exam_list')
        except CustomUser.DoesNotExist:
            return render(request, 'exams/sign_in.html', {'error': 'Invalid credentials'})
    return render(request, 'exams/sign_in.html')

def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    return render(request, 'exams/exam_detail.html', {'exam': exam})

def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'exams/exam_list.html', {'exams': exams})

#def exam_list(request):
   # with connection.cursor() as cursor:
       # cursor.execute("SELECT * FROM exams_exam")
       # results = cursor.fetchall()

        # Structure the results as a list of dictionaries for easier use in templates
        #exams = [
          #  {'id': row[0], 'name': row[1], 'description': row[2], 'date_created': row[3]}
           # for row in results
       # ]

    return render(request, 'exams/exam_list.html', {'exams': exams})

def create_exam(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO exams_exam (name, description, date_created) VALUES (%s, %s, NOW())",
                [name, description]
            )

        return redirect('exam_list')

    return render(request, 'exams/create_exam.html')

@login_required
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'exams/create_question.html', {'form': form})

def take_exam(request, exam_id):
    exam = Exam.objects.get(id=exam_id)
    questions = Question.objects.filter(exam=exam)
    if request.method == 'POST':
        score = 0
        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option == question.correct_option:
                score += 1
        Result.objects.create(user=request.user, exam=exam, score=score)
        return redirect('exam_results')
    return render(request, 'exams/take_exam.html', {'exam': exam, 'questions': questions})

def submit_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    related_questions = Question.objects.filter(exam=exam)

    if request.method == 'POST':
        # Initialize score counter
        score = 0
        
        # Process the submitted answers
        # for question in exam.question_set.all():
        for question in exam.question_set.all():
            selected_answer = request.POST.get(f'answer_{question.id}')
            if selected_answer == question.correct_option:
                score += 1

        # Save the result
        result = Result.objects.create(exam=exam, score=score)

        # Redirect to the exam result page
        return redirect('exam_result', exam_id=exam.id, score=score)

    return render(request, 'exams/take_exam.html', {'exam': exam})


def exam_result(request):
    results = Result.objects.filter(user=request.user)
    return render(request, 'exams/exam_result.html', {'results': results})


# Create your views here.
