from django.db import models
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    title = models.CharField(max_length=50, verbose_name='Тема письма')
    text = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class Client(models.Model):
    email = models.EmailField(verbose_name='Почта')
    fio = models.CharField(max_length=100, verbose_name='Ф.И.О')
    comment = models.TextField(verbose_name='Комментарий')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', null=True)

    def __str__(self):
        return f'ФИО: {self.fio}, почта: {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Newsletter(models.Model):
    class Periodicity(models.TextChoices):
        DAILY = 'Раз в день'
        WEEKLY = 'Раз в неделю'
        MONTHLY = 'Раз в месяц'

    class Status(models.TextChoices):
        FINISHED = 'завершена'
        CREATED = 'создана'
        LAUNCHED = 'запущена'

    first_newsletter = models.DateTimeField(auto_now_add='True', verbose_name='Дата и время первой рассылки')
    last_newsletter = models.DateTimeField(auto_now='True', verbose_name='Дата и время последней рассылки')
    periodicity = models.CharField(max_length=20, verbose_name='Периодичность', choices=Periodicity.choices)
    status = models.CharField(max_length=20, verbose_name='Статус рассылки', choices=Status.choices, default=Status.CREATED)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщения', null=True)
    clients = models.ManyToManyField(Client, verbose_name='Клиенты рассылки')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', null=True)

    def __str__(self):
        return f'Время: {self.first_newsletter} - {self.last_newsletter}, периодичность: {self.periodicity}, Статус: {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            (
                'view_all_newsletters',
                'Can view all newsletters'
            ),
            (
                'deactivate_newsletter',
                'Can deactivate newsletters'
            ),
        ]


class Logs(models.Model):
    attempt = models.BooleanField(verbose_name='Статус попытки')
    attempt_time = models.DateTimeField(verbose_name='Дата и время последней попытки')
    response = models.CharField(max_length=100, verbose_name='Ответ почтового сервера', **NULLABLE)
    newsletter = models.ForeignKey(Newsletter, verbose_name='Название рассылки', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True)

    def __str__(self):
        return f"Attempt: {self.attempt}, Time: {self.attempt_time}, Response: {self.response}"

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'



