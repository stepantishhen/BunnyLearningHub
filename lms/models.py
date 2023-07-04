from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

STATUS = [
    ('ns', 'не сдано'),
    ('s', 'сдано'),
    ('rat', 'оценено')]


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название курса', blank=False)
    description = models.CharField(max_length=255, verbose_name='Описание курса', blank=True)
    author = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, verbose_name='Автор курса', related_name='authored_courses')
    picture = models.ImageField(upload_to='picrures/', verbose_name='Изображение курса')
    is_publish = models.BooleanField(default=True, verbose_name='Опубликовано')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    users = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Курсы'
        verbose_name = 'Курс'
        ordering = ['name', 'author', '-time_create', '-is_publish']


class MessageCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    message = models.TextField(verbose_name='Сообщение')
    is_publish = models.BooleanField(default=True, verbose_name='Опубликовано')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='Курс')

    def __str__(self):
        return f'{self.message} ({self.user})'

    class Meta:
        verbose_name_plural = 'Сообщения курсов'
        verbose_name = 'Сообщение курса'
        ordering = ['-time_create', 'user', '-is_publish']


class MessageModule(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    message = models.TextField(verbose_name='Сообщение')
    is_publish = models.BooleanField(default=True, verbose_name='Опубликовано')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    module = models.ForeignKey('Module', on_delete=models.CASCADE, verbose_name='Модуль')

    def __str__(self):
        return f'{self.message} ({self.user})'

    class Meta:
        verbose_name_plural = 'Сообщения модулей'
        verbose_name = 'Сообщение модуля'
        ordering = ['-time_create', 'user', '-is_publish']


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
        ordering = ['name', 'course', '-time_create', 'is_publish']


class Homework(models.Model):
    content = RichTextUploadingField(models.Model)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name='Модуль')
    is_publish = models.BooleanField(default=True, verbose_name='Опубликовано')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    deadline = models.DateTimeField(verbose_name='Дедлайн')

    def __str__(self):
        return self.module.name

    class Meta:
        verbose_name_plural = 'Домашние задания'
        verbose_name = 'Домашнее задание'
        ordering = ['deadline', 'module', 'is_publish']


class HomeworkAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, verbose_name='Домашнее задание')
    google_disk_url_folder = models.URLField(verbose_name='Ссылка на папку в Google диске')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    mark = models.IntegerField(null=True, default=0, verbose_name='Оценка')
    status = models.CharField(max_length=255, default='не сдано',
                              choices=STATUS, verbose_name='Статус')

    def __str__(self):
        return f'{self.user.username} - {self.homework.module.name}'

    class Meta:
        verbose_name_plural = 'Ответы на домашние задания'
        verbose_name = 'Ответ на домашнее задание'
        ordering = ['-time_create', 'user', 'homework', 'status']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    description = models.CharField(max_length=255, verbose_name='Описание')
    social_link = models.URLField(verbose_name='Ссылка на соц. сеть', null=True, blank=True)
    avatar = models.ImageField(upload_to='picrures/', verbose_name='Аватарка')

    def __str__(self):
        return f'{self.user.username}'
    class Meta:
        verbose_name_plural = 'Профили'
        verbose_name = 'Профиль'
        ordering = ['user']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()