from django.shortcuts import render, redirect
from django.template import loader
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from .forms import buyform, nomer, boolform, Searchform, UserRegistration, User_login_form, OrderModelform
from .models import buy, nomerz, category, OrderModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import aggregates, F, Q
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import CategorySerializer
from rest_framework.response import Response

def HomePage(request):
    if request.method == 'POST':
        form = Searchform(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            print(search)
            buys = buy.objects.filter(Q(Q(title__contains=search)| Q(content__contains=search)) & Q(ordered=False))
            return render(request, 'glpage/indexb.html', {'buys': buys, 'title': 'Главная', 'form': form})
    else:
        form = Searchform()
        buys = buy.objects.filter(remain__gt = 0)
        return render(request, 'glpage/indexb.html', {'buys': buys, 'title': 'Главная', 'form': form})


def about(request):
    return render(request, 'glpage/about.html')


def create(request):
    if request.method == 'POST':
        form = buyform(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            created = buy.objects.create(**form.cleaned_data)
            return redirect('home')
    else:
        form = buyform()
    context = {'form': form, }
    return render(request, 'glpage/create.html', context)


def order(request, tovar_id):
    tovar = buy.objects.get(pk=tovar_id)
    current_user = request.user
    if tovar.ordered_by.filter(pk=request.user.id):
        tovar.ordered_by.remove(current_user)
        tovar.remain+=1
    else:
        tovar.ordered_by.add(current_user)
        if not tovar.ordered:
            tovar.ordered = True
        tovar.remain-=1
    if not tovar.ordered_by.all():
        tovar.ordered = False
    tovar.save()
    return redirect(tovar)

class TovarByCat(ListView):
    model = buy
    template_name = 'glpage/category.html'
    context_object_name = 'buys'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return buy.objects.filter(category=self.kwargs['category_id'], ordered=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = category.objects.get(pk=self.kwargs['category_id'])
        return context




def tovar_page(request,tovar_id):
    tovar = get_object_or_404(buy, pk=tovar_id)
    current_user = request.user
    if tovar.ordered_by.filter(pk=current_user.id):
        ordered_or_not = 'Удалить из корзины'
    else:
        ordered_or_not = 'Добавить в корзину'
    context = {'tovar': tovar, 'ordered_or_not': ordered_or_not}
    return render(request, 'glpage/tovar.html', context)


class TovarPage(DetailView):
    model = buy
    template_name = 'glpage/tovar.html'
    context_object_name = 'tovar'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


class Packet(ListView):
    model = buy
    context_object_name = 'buys'
    template_name = 'glpage/order.html'

    def get_queryset(self):
        return buy.objects.filter(Q(ordered=True) & Q())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзина'
        price_order = 0
        for item in buy.objects.filter(ordered=True):
            price_order+=item.price
        context['price_order'] = price_order
        return context

def user_Packet(request):
    current_user = request.user
    ordered_things = current_user.buy_set.all()
    price_packet = 0
    for item in ordered_things:
        price_packet += item.price
    context = {'buys':ordered_things, 'user':current_user, 'price_order': price_packet} # price_order
    return render(request, 'glpage/order.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registered')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Not registered')
    else:
        form = UserRegistration()
    context = {'form': form, }
    return render(request, 'glpage/register.html', context)

def user_login(request):
    if request.method == 'POST':
        form = User_login_form(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = User_login_form()
    context = {'form': form}
    return render(request, 'glpage/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')

def orderingprocess(request):
    current_user = request.user
    ordered_things = current_user.buy_set.all()
    if request.method == 'POST':
        form = OrderModelform(request.POST)
        if form.is_valid():
            order = OrderModel(ordered_by_user=current_user.username,ordered_by_name=form.cleaned_data['ordered_by_name'], ordered_by_phone = form.cleaned_data['ordered_by_phone'], transport = form.cleaned_data['transport'], address = form.cleaned_data['address'])
            order.save()
            for item in current_user.buy_set.all():
                order.ordered_things.add(item)
            order.save()
            return redirect('home')
    else:
        form = OrderModelform()
    context = {
        'form':form,
        'title':'Ordering',
        'buys': current_user.buy_set.all()
    }
    return render(request, 'glpage/ordering.html', context)

class catAPI(APIView):
    def get(self, request):
        return Response({'category':CategorySerializer(category.objects.all(), many=True).data})
