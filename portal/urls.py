from django.urls import path
from .views import PostList, PostDetail  # Импортируем созданное нами представление

urlpatterns = [
   # Т.к. наше объявленное представление является классом, а Django ожидает функцию,
   # нам надо представить этот класс в виде view. Для этого вызываем метод as_view.
   path('', PostList.as_view()),

   # pk — это первичный ключ новости, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostDetail.as_view()),
   # path('<int:id>', ProductDetail.as_view()),  # можем изменить с помощью pk_url_kwarg
]
