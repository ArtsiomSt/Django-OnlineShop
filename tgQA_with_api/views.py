from django.shortcuts import render, redirect
from .forms import QAform
from .models import *
from rest_framework.views import APIView
from .serializers import TGserializer
from rest_framework.response import Response

def listofq(request):
    questions = TelegramQA.objects.filter(is_answered = False)
    context = {
        'questions':questions,
        'title': 'Вопросы и ответы'
    }
    return render(request, 'tgQA/listofqa.html', context)

def answerquestion(request, question_id):
    question = TelegramQA.objects.get(pk=question_id)
    if question.is_answered:
        is_ans = 'На вопрос уже дан ответ'
    else:
        is_ans = 'На вопрос еще нет ответа'

    if request.method == 'POST':
        form = QAform(request.POST)
        if form.is_valid():
            TelegramQA.objects.filter(pk=question_id).update(answer=form.cleaned_data['answer'])
            TelegramQA.objects.filter(pk=question_id).update(is_answered=form.cleaned_data['yorn'])
            return redirect('listofq')
    else:
        form = QAform()
    context = {
        'question': question,
        'title': 'Answer for q',
        'is_ans': is_ans,
        'form': form,
        'label': 'Оформление заказа'
    }
    return render(request, 'tgQA/answerforquestion.html', context)

class Createtgq(APIView):
    def get(self,request, *args, **kwargs):
        username = kwargs.get("username", None)
        if not username:
            return Response({"error": 'Method net'})
        try:
            questions_of_user = TelegramQA.objects.filter(tguser = username)
        except:
            return Response({"error": 'Model net'})
        serializer = TGserializer(questions_of_user, many=True)
        return Response({'userquestions': serializer.data})

    def post(self, request):
        serializer = TGserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'created':serializer.data})

    def delete(self, request, *arg, **kwargs):
        username = kwargs.get("username", None)
        if not username:
            return Response({"error": 'Method net'})
        try:
            TelegramQA.objects.filter(tguser=username).delete()
        except:
            return Response({"error": 'Model net'})
        return Response({'deleted': 'deleted ' + username})


