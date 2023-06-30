from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
# Импортируем дженерики для представлений
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Subscriber
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):  # Класс-представление для показа списка наших объектов
    model = Post  # Указываем модель, которая будет использоваться в представлении
    ordering = '-create_time'  # Указываем сортировку списка
    template_name = 'posts.html'  # Указываем имя шаблона, которое будет использоваться
    context_object_name = 'posts'  # Так мы будем обращаться к списку в HTML коде
    paginate_by = 10  # вот так мы можем указать количество записей на странице


class PostListSearch(PostList, ListView):
    # model = Post
    # ordering = '-create_time'
    template_name = 'posts_search.html'
    # context_object_name = 'posts'
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()  # Получаем обычный запрос
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict.
        # Сохраняем нашу фильтрацию в объекте класса, чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs  # Возвращаем из функции отфильтрованный список товаров

    def post(self, request, *args, **kwargs):
        selected_category = self.request.GET.get('category', False)
        category = Category.objects.get(pk=selected_category)

        if not Subscriber.objects.filter(user_id=self.request.user.pk).exists():
            Subscriber.objects.create(user_id=self.request.user.pk)

        subscriber = Subscriber.objects.get(user_id=self.request.user.pk)
        subscriber.category.add(category)

        return HttpResponseRedirect("/news/")


class PostDetail(DetailView):
    model = Post  # Модель всё та же, но мы хотим получать информацию по отдельной новости
    template_name = 'post.html'  # Используем другой шаблон
    context_object_name = 'post'  # Название объекта, в котором будет выбранная новость
    # Будет выводить новость как, как мы описали его в методе __str__
    # Мы также можем указать Django как называть идентификатор в urlpatterns (по-умолчанию стоит pk)
    # pk_url_kwarg = 'id'


class PostCreate(CreateView, PermissionRequiredMixin, LoginRequiredMixin,):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('portal.add_post',)


class PostUpdate(UpdateView, PermissionRequiredMixin, LoginRequiredMixin,):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('portal.edit_post',)


class PostDelete(DeleteView, PermissionRequiredMixin, LoginRequiredMixin,):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('portal.delete_post',)


class CategoryList(ListView):
    model = Category
    template_name = 'categories_list.html'
    ordering = 'name'
    context_object_name = 'categories'
