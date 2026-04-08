from django.db import models

# Create your models here.
class Book(models.Model):
    COVERS = [
        ('hardcover', 'Hardcover'),
        ('paperback', 'Paperback'),
        ('ebook', 'Ebook'),
        ('audiobook', 'Audiobook'),
    ]

    LANGUAGES = [
        ('english', 'English'),
        ('spanish', 'Spanish'),
        ('polish', 'Polish'),
        ('german', 'German'),
        ('hebrew', 'Hebrew'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    publication_date = models.DateField()
    pages = models.IntegerField()
    cover = models.CharField(max_length=20, choices=COVERS)
    language = models.CharField(max_length=20, choices=LANGUAGES)
    is_read = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
# class Author(models.Model):

# class Publisher(models.Model):

# class Genre(models.Model):

# class Series(models.Model):

# class Topic(models.Model):

# class Category(models.Model):

# class Note(models.Model):