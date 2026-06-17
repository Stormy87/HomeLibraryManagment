from django.contrib import admin

from .models import Author, Book, Category, Genre, Note, Publisher, Series, Topic

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Series)
admin.site.register(Genre)
admin.site.register(Topic)
admin.site.register(Category)
admin.site.register(Note)
