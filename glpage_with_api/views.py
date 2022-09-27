def HomePage(request):
    print(request.__dict__)
    for item in request.GET.values():
        print(item)
    if request.user.is_authenticated:
        cur_user = UserProfile.objects.get(username=request.user.username)
        if not cur_user.auth_token:
            logout(request)
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
    print(request.user)
    return render(request, 'glpage/about.html')


def create(request):
    if request.method == 'POST':
        form = buyform(request.headers)
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
        title = category.get_cat_id_by_slug(self.kwargs['category_id'])
        current_cat = category.objects.get(title=title)
        context['title']=category.objects.get(pk=current_cat.pk)
        return context

    def get_queryset(self):
        title = category.get_cat_id_by_slug(self.kwargs['category_id'])
        current_cat = category.objects.get(title=title)
        return buy.objects.filter(category=current_cat.pk, ordered=False)




def tovar_page(request,tovar_id):
    tovar = get_object_or_404(buy, pk=tovar_id)
    current_user = request.user
    if tovar.ordered_by.filter(pk=current_user.id):
        ordered_or_not = 'Удалить из корзины'
    else:
        ordered_or_not = 'Добавить в корзину'
    context = {'tovar': tovar, 'ordered_or_not': ordered_or_not}
    return render(request, 'glpage/tovar.html', context)


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
            print(form.cleaned_data)
            form.save()
            messages.success(request, 'Registered')
            username = form.data['username']
            password = form.data['password1']
            user_login_form = {
                "username" : username,
                "password" : password,
            }
            url = "http://127.0.0.1:8000/auth/token/login"
            resp = requests.post(url, data=user_login_form)
            if 'auth_token' in resp.json():
                user = authenticate(request, username=username, password=password)
                login(request, user)
                print(resp.json()['auth_token'])
                if UserProfile.objects.filter(username=username):
                    print(UserProfile.objects.filter(username=username))
                    curuserprof = UserProfile.objects.get(username=username)
                    curuserprof.auth_token = resp.json()['auth_token']
                    curuserprof.save()
                else:
                    UserProfile.objects.create(username=username, user=request.user, auth_token=resp.json()['auth_token'])
                return redirect('home')
        else:
            messages.error(request, 'Not registered')
    else:
        form = UserRegistration()
    context = {'form': form, }
    return render(request, 'glpage/register.html', context)


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
    permission_classes = (IsAdminUser, )
    def get(self, request):
        return Response({'category':CategorySerializer(category.objects.all(), many=True).data})


def loginbyapi(request):
    message = 'Вход'
    if request.method == 'POST':
        form = LoginByAPIForm(request.POST)
        if form.is_valid():
            username = form.data['username']
            password = form.data['password']
            print(form.cleaned_data['choice'])
            user_login_form = {
                "username" : username,
                "password" : password,
            }
            url = "http://127.0.0.1:8000/auth/token/login"
            resp = requests.post(url, data=user_login_form)
            if 'auth_token' in resp.json():
                user = authenticate(request, username=username, password=password)
                login(request, user)
                print(resp.json()['auth_token'])
                if UserProfile.objects.filter(username=username):
                    print(UserProfile.objects.filter(username=username))
                    curuserprof = UserProfile.objects.get(username=username)
                    curuserprof.auth_token = resp.json()['auth_token']
                    curuserprof.save()
                else:
                    UserProfile.objects.create(username=username, user=request.user, auth_token=resp.json()['auth_token'])
                return redirect('home')
            else:
                message = 'You have failed you loging'
    else:
        form = LoginByAPIForm()
    context = {
        'messaga':message,
        'form':form
    }
    return render(request, 'glpage/loginbyapi.html', context)


def logoutbyapi(request):
    if not request.user.is_authenticated:
        return redirect('home')
    url = "http://127.0.0.1:8000/auth/token/logout"
    currpofile = UserProfile.objects.get(username=request.user.username)
    header = 'Token '+currpofile.auth_token
    currpofile.auth_token = ''
    currpofile.save()
    headers = {"Authorization": header}
    resp = requests.post(url, headers=headers)
    logout(request)
    return redirect('home')


def study(request, number):
    tov = buy.objects.get(pk=22)
    context = {
        'number': number,
        'object': tov,
        'title': 'Name'
    }
    return render(request, 'glpage/study1.html', context)
