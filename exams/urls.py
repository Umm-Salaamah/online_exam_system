from django.urls import path
from . import views
from .views import sign_in

urlpatterns = [
    path('', sign_in, name='sign_in'),
    path('examList/', views.exam_list, name='exam_list'),  # List exams at /exams/
    
    path('create_exam/', views.create_exam, name='create_exam'),  # Ensure this line is present
    path('<int:exam_id>/', views.exam_detail, name='exam_detail'), 
    path('<int:exam_id>/', views.take_exam, name='take_exam'),
    path('take_exam/<int:exam_id>/', views.take_exam, name='take_exam'),
    path('create_question/', views.create_question, name='create_question'),
    path('exam_result/', views.exam_result, name='exam_result'),
    path('submit_exam/<int:exam_id>/', views.submit_exam, name='submit_exam'),  # Add this line
    path('exam_result/<int:exam_id>/<slug:score>/', views.exam_result, name='exam_result'),
   
]
