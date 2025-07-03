from django.db import models
from django.urls import reverse
from django.conf import settings
from slugify import slugify
# Create your models here.
class Artist(models.Model):
    name        = models.CharField(verbose_name="Имя артиста", max_length=255, unique=True)
    slug        = models.SlugField(verbose_name="URL", max_length=255, unique=True, blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    avatar      = models.ImageField(
        verbose_name="Аватар",
        upload_to="artist_avatars/",
        blank=True,
        null=True
    )
    homepage_image = models.ImageField(default='default_homepage.png', upload_to='homepages/')

    class Meta:
        ordering = ["name"]
        verbose_name = "Артист"
        verbose_name_plural = "Артисты"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("artists:artist-detail", args=[self.slug or self.id])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ArtistLink(models.Model):
    artist   = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="links"
    )
    platform = models.CharField(verbose_name="Платформа", max_length=100)
    url       = models.URLField(verbose_name="Ссылка")

    class Meta:
        unique_together = ("artist", "platform", "url")
        verbose_name = "Ссылка артиста"
        verbose_name_plural = "Ссылки артиста"

    def __str__(self):
        return f"{self.artist.name} — {self.platform}"
    

class ArtistClaimed(models.Model):
    """
    Заявки на «присвоение» артиста,
    отправлены пользователями и модераторами обрабатываются
    """
    class Status(models.TextChoices):
        PENDING  = "pending",  "В ожидании"
        APPROVED = "approved", "Подтверждена"
        REJECTED = "rejected", "Отклонена"

    user        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="artist_claims"
    )
    artist      = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="claims"
    )
    status      = models.CharField(
        verbose_name="Статус",
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    moderated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="artist_claims_moderated"
    )
    created_at  = models.DateTimeField(verbose_name="Дата подачи", auto_now_add=True)
    updated_at  = models.DateTimeField(verbose_name="Дата изменения статуса", auto_now=True)

    class Meta:
        unique_together = ("user", "artist")
        ordering = ["-created_at"]
        verbose_name = "Заявка артиста"
        verbose_name_plural = "Заявки артистов"

    def __str__(self):
        return f"{self.user.username} → {self.artist.name} ({self.get_status_display()})"