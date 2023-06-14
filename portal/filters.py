from django.forms import DateInput
from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post, Category


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Любая'
    )
    create_time = DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        label='Статьи позднее:',
        lookup_expr='date__gt'
    )

    class Meta:
        # В Meta классе мы должны указать Django модель, в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели будет производиться фильтрация.
        fields = {
            'title': ['icontains'],  # поиск по названию
            'author': ['exact'],     # количество товаров должно быть больше или равно
        }
