from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class buy(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d', blank=True, null=True)
    ordered = models.BooleanField(default=False)
    ordered_by = models.ManyToManyField(User,  blank=True, null=True)
    remain = models.FloatField(default=0)

    def get_absolute_url(self):
        return reverse('tovar', kwargs={"tovar_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class nomerz(models.Model):
    num = models.FloatField(null=True, blank=True)

class category(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name='Тип')
    slug = models.SlugField(max_length= 50, unique=True, verbose_name='URL', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    @classmethod
    def get_cat_id_by_slug(cls, slug):
        allslugs = {
            'audiotech':'Аудиотехника',
            'videotech':'Видеотехника',
            'vishisltech':'Вычислилельная'
        }
        title = allslugs[slug]
        return title

    def __str__(self):
        return self.title

class OrderModel(models.Model):
    ordered_by_user = models.CharField(max_length=50, blank=True, null=True)
    ordered_by_name = models.CharField(max_length=50, blank=True, null=True)
    ordered_by_phone = models.CharField(max_length=15)
    transport = models.ForeignKey('Transport', on_delete=models.PROTECT)
    address = models.TextField(blank=True, null=True)
    ordered_things = models.ManyToManyField(buy)

class Transport(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name='Тип доставки')

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    username = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    auth_token = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username
