from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название курса')
    description = models.CharField(max_length=255, verbose_name='Описание курса')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор курса')
    social_link = models.URLField(verbose_name='Ссылка на соц. сеть', null=True, blank=True)
    picture = models.ImageField(upload_to='picrures/', verbose_name='Изображение курса')
    is_publish = models.BooleanField(default=True, verbose_name='Опубликовано')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Курсы'
        verbose_name = 'Курс'
        ordering = ['-time_create']


class Topic(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название темы")
    description = models.CharField(max_length=255, verbose_name="Описание темы")

    def __str__(self):
        return f'{self.title} - {self.description}'

    class Meta:
        verbose_name_plural = 'Темы'
        verbose_name = 'Тема'
        ordering = ['-title']


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    is_publish = models.BooleanField(default=True, verbose_name='Опубликовано')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    def __str__(self):
        return f'{self.user.username} - {self.message}'

    class Meta:
        verbose_name_plural = 'Сообщения'
        verbose_name = 'Сообщение'
        ordering = ['-time_create']


class UserCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    def __str__(self):
        return f'{self.user.username} - {self.course.name}'

    class Meta:
        verbose_name_plural = 'Курсы пользователей'
        verbose_name = 'Курс пользователя'
        ordering = ['-time_create']


class Module(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название модуля')
    description = models.CharField(max_length=255, verbose_name='Описание модуля')
    content = RichTextUploadingField(models.Model)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    is_publish = models.BooleanField(default=True, verbose_name='Опубликовано')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Модули'
        verbose_name = 'Модуль'
        ordering = ['-time_create']


class Homework(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название домашнего задания')
    description = models.CharField(max_length=255, verbose_name='Описание домашнего задания')
    content = RichTextUploadingField(models.Model)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name='Модуль')
    is_publish = models.BooleanField(default=True, verbose_name='Опубликовано')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    deadline = models.DateTimeField(verbose_name='Дедлайн')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Домашние задания'
        verbose_name = 'Домашнее задание'
        ordering = ['-time_create']


class HomeworkAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, verbose_name='Домашнее задание')
    google_disk_url_folder = models.URLField(verbose_name='Ссылка на папку в Google диске')
    is_publish = models.BooleanField(default=True, verbose_name='Опубликовано')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    mark = models.IntegerField(null=True, blank=True, verbose_name='Оценка')
    status = models.CharField(max_length=255, null=True, blank=True, verbose_name='Статус')

    def __str__(self):
        return f'{self.user.username} - {self.homework.name}'

    class Meta:
        verbose_name_plural = 'Ответы на домашние задания'
        verbose_name = 'Ответ на домашнее задание'
        ordering = ['-time_create']
