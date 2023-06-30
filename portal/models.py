from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):  # Сущность "автор"
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь O2O с моделью User
    rating = models.IntegerField(default=0)  # Рейтинг автора

    def update_rating(self):  # Метод, который считает рейтинг автора
        self.rating = 0
        author_posts = Post.objects.filter(author=self)  # Рейтинг постов автора
        for post in author_posts:
            self.rating += post.rating * 3

        author_comments = Comment.objects.filter(user=self.user.pk)
        for comment in author_comments:
            self.rating += comment.rating

        for post in author_posts:
            comments = Comment.objects.filter(post=post)
            for comment in comments:
                self.rating += comment.rating

        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):  # Сущность "категория"
    name = models.CharField(max_length=255, unique=True)  # Название категории

    def __str__(self):
        return self.name


class Post(models.Model):  # Сущность "статься/пост"
    news, article = 'NEWS', 'ARTICLE'  # Выбор типа ограничен
    POSITIONS = [
        (news, 'НОВОСТЬ'),
        (article, 'СТАТЬЯ')
    ]

    type = models.CharField(max_length=7, choices=POSITIONS, default=news)  # Тип объекта с выбором
    create_time = models.DateTimeField(auto_now_add=True)  # Автоматическая дата/время создания
    title = models.CharField(max_length=255)  # Заголовок поста
    content = models.TextField()  # Текст поста
    rating = models.IntegerField(default=0)  # Рейтинг поста
    category = models.ManyToManyField(Category, through='PostCategory')  # Связь категория M2M через PostCategory
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Связь O2M с моделью автор

    def like(self):  # Like, увеличивает рейтинг на 1
        self.rating += 1
        self.save()

    def dislike(self):  # Dislike, уменьшает рейтинг на 1
        self.rating -= 1
        self.save()

    def preview(self):  # Возвращает первые 124 символа текста поста и добавляет многоточие
        text = str(self.content)
        if len(text) >= 125:
            return text[:124] + '...'
        else:
            return text

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):  # Промежуточная таблица для связи M2M между постами и категориями
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Связь O2M с постами
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Связь O2M с категориями


class Comment(models.Model):  # Сущность "комментарий"
    content = models.CharField(max_length=1000)  # Текст комментария
    create_time = models.DateTimeField(auto_now_add=True)  # Дата/время создания комментария
    rating = models.IntegerField(default=0)  # Рейтинг комментария
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Связь с постом. При удалении поста удалить комментарий
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с автором комментария

    def like(self):  # Like, увеличивает рейтинг на 1
        self.rating += 1
        self.save()

    def dislike(self):  # Dislike, уменьшает рейтинг на 1
        self.rating -= 1
        self.save()


class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return f'{User.objects.get(pk=self.user_id)}'
