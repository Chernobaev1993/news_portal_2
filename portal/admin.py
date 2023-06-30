from django.contrib import admin
from .models import Post, Category, PostCategory, Subscriber

admin.site.register(Category)  # Регистрируем модели, чтобы видеть их в админ панели
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Subscriber)

