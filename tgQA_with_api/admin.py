from django.contrib import admin
from .models import *

class AdminQA(admin.ModelAdmin):
    list_display = ('id', 'tguser', 'question', 'answer', 'is_answered')

admin.site.register(TelegramQA, AdminQA)
