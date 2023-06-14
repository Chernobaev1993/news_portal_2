from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):  # Класс для быстрого создания форм на основе конкретных моделей
    content = forms.CharField(min_length=20)  # Можно сделать так, чтобы проверять длину описания и не писать clean

    class Meta:
        model = Post  # Саму модель прописываем в мета классе
        # fields = '__all__'  # Здесь мы указали, что хотим использоваться все поля модели, кроме pk
        fields = [  # Либо можем сами редактировать
            'type',
            'title',
            'content',
            'category',
            'author',
        ]

        # Если мы хотим сделать свои собственные проверки, нам нужно переопределить метод clean в форме
    def clean(self):
        # Вызовем в нашем методе clean из родительского класса и сохраним данные формы в cleaned_data.
        cleaned_data = super().clean()

        description = cleaned_data.get("description")
        name = cleaned_data.get("name")
        # Добавляем проверку длины описания, смотри выше вариант получше
        # if description is not None and len(description) < 20:
        #     raise ValidationError({
        #         "description": "Описание не может быть менее 20 символов."
        #     })

        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data