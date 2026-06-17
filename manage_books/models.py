from django.contrib.auth.models import User
from django.db import models
import pytz


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    COVERS = [
        ('hardcover', 'Twarda oprawa'),
        ('paperback', 'Miękka oprawa'),
        ('ebook', 'E-book'),
        ('audiobook', 'Audiobook'),
    ]
    LANGUAGES = [
        ('english', 'Angielski'),
        ('polish', 'Polski'),
        ('spanish', 'Hiszpański'),
        ('french', 'Francuski'),
        ('german', 'Niemiecki'),
        ('other', 'Inny'),
    ]

    title = models.CharField(max_length=200)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.IntegerField()
    cover = models.CharField(max_length=20, choices=COVERS)
    language = models.CharField(max_length=20, choices=LANGUAGES)
    is_read = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books', null=True, blank=True)
    authors = models.ManyToManyField('Author', related_name='books', blank=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.RESTRICT)
    series = models.ForeignKey('Series', on_delete=models.RESTRICT, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='books')
    genres = models.ManyToManyField('Genre', related_name='books', blank=True)
    topics = models.ManyToManyField('Topic', related_name='books', blank=True)

    def __str__(self):
        return self.title


class Author(models.Model):
    TITLES = [
        ('ks', 'Ks.'),
        ('dr', 'Dr.'),
        ('prof', 'Prof.'),
        ('bp', 'Bp.'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=100)
    title = models.CharField(max_length=50, choices=TITLES, blank=True, null=True)

    def __str__(self):
        if self.alias:
            return f"{self.get_title_display() or ''} {self.alias} {self.last_name}".strip()
        return f"{self.get_title_display() or ''} {self.first_name} {self.last_name}".strip()


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=2, choices=pytz.country_names.items())
    founded_year = models.IntegerField()
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='series', blank=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='notes')

    def __str__(self):
        return f"Notatka do {self.book.title}"
