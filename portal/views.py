from django.shortcuts import render
from django.views.generic import ListView, DetailView  # Импортируем дженерики для представлений
from .models import Post


class PostList(ListView):  # Класс-представление для показа списка наших объектов
    model = Post  # Указываем модель, которая будет использоваться в представлении
    ordering = '-create_time'  # Указываем сортировку списка
    template_name = 'posts.html'  # Указываем имя шаблона, которое будет использоваться
    context_object_name = 'posts'  # Так мы будем обращаться к списку в HTML коде


class PostDetail(DetailView):
    model = Post  # Модель всё та же, но мы хотим получать информацию по отдельной новости
    template_name = 'post.html'  # Используем другой шаблон
    context_object_name = 'post'  # Название объекта, в котором будет выбранная новость
    # Будет выводить новость как, как мы описали его в методе __str__
    # Мы также можем указать Django как называть идентификатор в urlpatterns (по-умолчанию стоит pk)
    # pk_url_kwarg = 'id'
