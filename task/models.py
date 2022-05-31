from datetime import timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model


def _get_next_day():
    """
    TODO 7. Заметка должна иметь дату и время, по умолчанию +1 день от текущего, может быть изменена автором
    +1 день от текущего
    timezone из django выдаст текущую дату как и datetime, но с учетом временной зоны на сервере Django
    """
    return timezone.now() + timedelta(days=1)


class Task(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, _("Отложено")
        ACTIVE = 1, _("Активно")
        DONE = 2, _("Выполнено")
    title = models.CharField(max_length=256, verbose_name=_("Заголовок"))
    note = models.TextField(default="", verbose_name=_("Примечание"))
    status = models.IntegerField(  # TODO 4. Заметка должна иметь статус состояния, один из: ["Активно", "Отложено", "Выполнено"]
        default=Status.DRAFT,
        choices=Status.choices,
        verbose_name=_("Статус")
    )
    important = models.BooleanField(default=False, verbose_name=_("Важно"))  # TODO 5. Заметка должна иметь признак: "Важно"
    public = models.BooleanField(default=False, verbose_name=_("Публичная"))  # TODO 6 Заметка должна иметь признак: "Публичная"
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создана"))
    deadline = models.DateTimeField(
        default=_get_next_day,  # функция будет каждый раз вызываться при инициализации экземпляра
        verbose_name=_("Выполнить до"))
    author = models.ForeignKey(
        get_user_model(),  # получить модель из setting.py из переменной AUTH_USER_MODEL
        on_delete=models.CASCADE,  # если удаляется пользователь, то удалять все его записи
        editable=False,  # TODO 3. Изменить автора нельзя
        verbose_name=_("Автор")
    )
