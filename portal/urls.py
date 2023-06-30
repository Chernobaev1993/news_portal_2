from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail, PostListSearch, PostCreate, PostUpdate, PostDelete, CategoryList

urlpatterns = [
    # Т.к. наше объявленное представление является классом, а Django ожидает функцию,
    # нам надо представить этот класс в виде view. Для этого вызываем метод as_view.
    path('', PostList.as_view(), name='post_list'),

    # pk — это первичный ключ новости, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    # path('<int:id>', ProductDetail.as_view()),  # можем изменить с помощью pk_url_kwarg

    path('search/', PostListSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('categories/', CategoryList.as_view(), name='cat_list'),  # Список категорий
]
