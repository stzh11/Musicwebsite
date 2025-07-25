# Generated by Django 5.2.3 on 2025-07-01 20:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("artists", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Album",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="Название альбома"),
                ),
                (
                    "slug",
                    models.SlugField(max_length=255, unique=True, verbose_name="URL"),
                ),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                (
                    "released_date",
                    models.DateField(blank=True, null=True, verbose_name="Дата выхода"),
                ),
                (
                    "cover",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="album_covers/",
                        verbose_name="Обложка",
                    ),
                ),
                (
                    "is_verified",
                    models.BooleanField(default=False, verbose_name="Верифицирован"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата добавления"
                    ),
                ),
            ],
            options={
                "verbose_name": "Альбом",
                "verbose_name_plural": "Альбомы",
                "ordering": ["-released_date"],
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="Жанр"),
                ),
            ],
            options={
                "verbose_name": "Жанр",
                "verbose_name_plural": "Жанры",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Song",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="Название трека"),
                ),
                (
                    "slug",
                    models.SlugField(max_length=255, unique=True, verbose_name="URL"),
                ),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                (
                    "released_date",
                    models.DateField(blank=True, null=True, verbose_name="Дата выхода"),
                ),
                (
                    "lyrics",
                    models.TextField(blank=True, verbose_name="Текст оригинала"),
                ),
                (
                    "translation_lyrics",
                    models.TextField(blank=True, verbose_name="Перевод текста"),
                ),
                (
                    "cover",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="song_covers/",
                        verbose_name="Обложка",
                    ),
                ),
                (
                    "clip_url",
                    models.URLField(blank=True, verbose_name="Ссылка на клип"),
                ),
                (
                    "is_verified",
                    models.BooleanField(default=False, verbose_name="Верифицирован"),
                ),
                (
                    "yandex_music_url",
                    models.URLField(blank=True, verbose_name="Яндекс.Музыка URL"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата добавления"
                    ),
                ),
                (
                    "album",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="songs",
                        to="music.album",
                    ),
                ),
            ],
            options={
                "verbose_name": "Песня",
                "verbose_name_plural": "Песни",
                "ordering": ["-released_date"],
            },
        ),
        migrations.CreateModel(
            name="AlbumConnection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("singer", "Вокал"),
                            ("writer", "Автор текста"),
                            ("producer", "Продюсер"),
                        ],
                        max_length=20,
                        verbose_name="Роль",
                    ),
                ),
                (
                    "album",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="connections",
                        to="music.album",
                    ),
                ),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="album_connections",
                        to="artists.artist",
                    ),
                ),
            ],
            options={
                "verbose_name": "Связь «Альбом–Артист»",
                "verbose_name_plural": "Альбомы ↔ Артисты",
                "unique_together": {("album", "artist", "role")},
            },
        ),
        migrations.CreateModel(
            name="AlbumGenre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "album",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="album_genres",
                        to="music.album",
                    ),
                ),
                (
                    "genre",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="albums",
                        to="music.genre",
                    ),
                ),
            ],
            options={
                "verbose_name": "Жанр альбома",
                "verbose_name_plural": "Жанры альбома",
                "unique_together": {("album", "genre")},
            },
        ),
        migrations.CreateModel(
            name="SongConnection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("singer", "Вокал"),
                            ("writer", "Автор текста"),
                            ("producer", "Продюсер"),
                        ],
                        max_length=20,
                        verbose_name="Роль",
                    ),
                ),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="song_connections",
                        to="artists.artist",
                    ),
                ),
                (
                    "song",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="connections",
                        to="music.song",
                    ),
                ),
            ],
            options={
                "verbose_name": "Связь «Песня–Артист»",
                "verbose_name_plural": "Песни ↔ Артисты",
                "unique_together": {("song", "artist", "role")},
            },
        ),
        migrations.CreateModel(
            name="SongGenre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "genre",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="songs",
                        to="music.genre",
                    ),
                ),
                (
                    "song",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="song_genres",
                        to="music.song",
                    ),
                ),
            ],
            options={
                "verbose_name": "Жанр трека",
                "verbose_name_plural": "Жанр трека",
                "unique_together": {("song", "genre")},
            },
        ),
    ]
