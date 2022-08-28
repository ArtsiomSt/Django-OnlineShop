from django.contrib import admin
from .models import buy, nomerz, category, OrderModel, Transport

class  BuyAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'content', 'ordered', 'remain',)
    list_display_links = ('id', 'category')
    search_fields = ('title', 'content')
    list_editable = ('ordered', 'remain')

class  CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)

admin.site.register(buy, BuyAdmin)
admin.site.register(category, CategoryAdmin)
admin.site.register(Transport)
admin.site.register(OrderModel)
