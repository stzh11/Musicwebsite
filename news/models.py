from django.db import models


from django.db import models

class News(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок"
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True
    )
    img = models.ImageField(
        upload_to="news_images/",
        verbose_name="Изображение",
        blank=True,

    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео",
        blank=True, 
        null =True 
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        db_table = "news"
        ordering = ["-created_at"]
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title