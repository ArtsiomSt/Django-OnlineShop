from django.contrib import admin
from .views import  *
from django.urls import path, include

urlpatterns = [
    path('listofq', listofq, name='listofq'),
    path('question/<int:question_id>/', answerquestion, name='question'),
]
