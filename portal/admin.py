from django.contrib import admin
from .models import Post, Category, PostCategory

admin.site.register(Category)  # Регистрируем модели, чтобы видеть их в админ панели
admin.site.register(Post)
admin.site.register(PostCategory)
