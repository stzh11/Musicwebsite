from django.db import models
from django.urls import reverse

class Album(models.Model):
    title         = models.CharField(verbose_name="Название альбома", max_length=255)
    slug          = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description   = models.TextField(verbose_name="Описание", blank=True)
    released_date = models.DateField(verbose_name="Дата выхода", null=True, blank=True)
    cover         = models.ImageField(verbose_name="Обложка", upload_to="album_covers/", blank=True, null=True)
    is_verified   = models.BooleanField(verbose_name="Верифицирован", default=False)
    created_at = models.DateTimeField(
        verbose_name="Дата добавления",
        auto_now_add=True
    )

    class Meta:
        ordering = ["-released_date"]
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("album-detail", args=[self.slug])

class Song(models.Model):
    title              = models.CharField(verbose_name="Название трека", max_length=255)
    slug               = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description        = models.TextField(verbose_name="Описание", blank=True)
    album              = models.ForeignKey(
                            Album,
                            related_name="songs",
                            on_delete=models.SET_NULL,
                            null=True, blank=True
                         )
    released_date      = models.DateField(verbose_name="Дата выхода", null=True, blank=True)
    lyrics             = models.TextField(verbose_name="Текст оригинала", blank=True)
    translation_lyrics = models.TextField(verbose_name="Перевод текста", blank=True)
    cover              = models.ImageField(verbose_name="Обложка", upload_to="song_covers/", blank=True, null=True)
    clip_url           = models.URLField(verbose_name="Ссылка на клип", blank=True)
    is_verified        = models.BooleanField(verbose_name="Верифицирован", default=False)
    yandex_music_url   = models.URLField(verbose_name="Яндекс.Музыка URL", blank=True)
    created_at = models.DateTimeField(
        verbose_name="Дата добавления",
        auto_now_add=True
    )

    class Meta:
        ordering = ["-released_date"]
        verbose_name = "Песня"
        verbose_name_plural = "Песни"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("song-detail", args=[self.slug])


class Genre(models.Model):
    name = models.CharField(verbose_name="Жанр", max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class SongGenre(models.Model):
    song  = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="song_genres")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="songs")

    class Meta:
        unique_together = ("song", "genre")
        verbose_name = "Жанр трека"
        verbose_name_plural = "Жанр трека"

    def __str__(self):
        return f"{self.song.title} — {self.genre.name}"


class AlbumGenre(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="album_genres")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="albums")

    class Meta:
        unique_together = ("album", "genre")
        verbose_name = "Жанр альбома"
        verbose_name_plural = "Жанры альбома"

    def __str__(self):
        return f"{self.album.title} — {self.genre.name}"
    

class AlbumConnection(models.Model):
    class Role(models.TextChoices):
        SINGER    = "singer", "Вокал"
        WRITER    = "writer", "Автор текста"
        PRODUCER  = "producer", "Продюсер"

    album  = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="connections")
    artist = models.ForeignKey("artists.Artist", on_delete=models.CASCADE, related_name="album_connections")
    role   = models.CharField(verbose_name="Роль", max_length=20, choices=Role.choices)

    class Meta:
        unique_together = ("album", "artist", "role")
        verbose_name = "Связь «Альбом–Артист»"
        verbose_name_plural = "Альбомы ↔ Артисты"

    def __str__(self):
        return f"{self.album.title} — {self.artist.name} ({self.role})"
    

class SongConnection(models.Model):
    class Role(models.TextChoices):
        SINGER    = "singer", "Вокал"
        WRITER    = "writer", "Автор текста"
        PRODUCER  = "producer", "Продюсер"
        # при необходимости можно добавить новые роли

    song   = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="connections")
    artist = models.ForeignKey("artists.Artist", on_delete=models.CASCADE, related_name="song_connections")
    role   = models.CharField(verbose_name="Роль", max_length=20, choices=Role.choices)

    class Meta:
        unique_together = ("song", "artist", "role")
        verbose_name = "Связь «Песня–Артист»"
        verbose_name_plural = "Песни ↔ Артисты"

    def __str__(self):
        return f"{self.song.title} — {self.artist.name} ({self.role})"