# suggestions/models.py
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class EditSuggestion(models.Model):
    class Status(models.TextChoices):
        PENDING  = "pending",  "В ожидании"
        APPROVED = "approved", "Одобрено"
        REJECTED = "rejected", "Отклонено"

    # --- универсальная ссылка на объект (song, album, artist и т.п.) ---
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="Тип объекта"
    )
    object_id = models.PositiveIntegerField(verbose_name="ID объекта")
    content_object = GenericForeignKey("content_type", "object_id")

    # --- что именно меняют ---
    field_name   = models.CharField(
        max_length=100,
        verbose_name="Поле для правки",
        help_text="Например: title, description, cover, lyrics и т.п."
    )
    old_value    = models.TextField(
        verbose_name="Старое значение",
        blank=True,
        help_text="Автозаполняется при создании, но можно оставить пустым"
    )
    new_value    = models.TextField(
        verbose_name="Предлагаемое значение",
    )

    # --- кто и когда предложил / обработал ---
    suggested_by   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="edit_suggestions",
        verbose_name="Кто предложил"
    )
    moderated_by   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="edit_suggestions_moderated",
        verbose_name="Кто подтвердил/отклонил"
    )
    status       = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Статус"
    )
    created_at   = models.DateTimeField(auto_now_add=True, verbose_name="Когда предложено")
    updated_at   = models.DateTimeField(auto_now=True,     verbose_name="Когда изменён статус")

    class Meta:
        verbose_name = "Предложение правки"
        verbose_name_plural = "Предложения правок"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.get_status_display()}: "
            f"{self.content_type.app_label}.{self.content_type.model} "
            f"#{self.object_id} «{self.field_name}»: «{self.new_value[:30]}…»"
        )
